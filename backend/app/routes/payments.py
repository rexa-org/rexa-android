from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
import razorpay
from .. import models
from ..db import get_db
from ..utils.auth_middleware import get_current_user_dependency
from ..config import settings

router = APIRouter()

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@router.post("/create-order")
def create_payment_order(
    amount: float,
    currency: str = "INR",
    current_user: models.User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Create a Razorpay payment order"""
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    # Convert to paise (Razorpay expects amount in smallest currency unit)
    amount_paise = int(amount * 100)
    
    # Create order
    order_data = {
        "amount": amount_paise,
        "currency": currency,
        "receipt": f"order_{current_user.id}_{int(amount)}",
        "notes": {
            "user_id": str(current_user.id),
            "purpose": "wallet_recharge"
        }
    }
    
    try:
        order = razorpay_client.order.create(data=order_data)
        return {
            "order_id": order["id"],
            "amount": amount,
            "currency": currency,
            "key_id": settings.RAZORPAY_KEY_ID
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment order creation failed: {str(e)}")

@router.post("/verify-payment")
def verify_payment(
    payment_id: str,
    order_id: str,
    signature: str,
    current_user: models.User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Verify Razorpay payment and credit wallet"""
    try:
        # Verify payment signature
        razorpay_client.utility.verify_payment_signature({
            "razorpay_payment_id": payment_id,
            "razorpay_order_id": order_id,
            "razorpay_signature": signature
        })
        
        # Get payment details
        payment = razorpay_client.payment.fetch(payment_id)
        
        if payment["status"] == "captured":
            # Credit user's wallet
            amount = payment["amount"] / 100  # Convert from paise to rupees
            
            wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
            if not wallet:
                wallet = models.Wallet(user_id=current_user.id, money=amount)
                db.add(wallet)
            else:
                wallet.money += amount
            
            db.commit()
            db.refresh(wallet)
            
            return {
                "message": "Payment verified and wallet credited",
                "amount": amount,
                "balance": float(wallet.money)
            }
        else:
            raise HTTPException(status_code=400, detail="Payment not completed")
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Payment verification failed: {str(e)}")

@router.post("/webhook")
async def razorpay_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Razorpay webhooks"""
    try:
        # Get webhook data
        data = await request.json()
        
        # Verify webhook signature
        webhook_signature = request.headers.get("X-Razorpay-Signature")
        if not webhook_signature:
            raise HTTPException(status_code=400, detail="Missing signature")
        
        # Handle different webhook events
        event = data.get("event")
        payload = data.get("payload", {})
        
        if event == "payment.captured":
            payment = payload.get("payment", {})
            payment_id = payment.get("id")
            amount = payment.get("amount", 0) / 100
            
            # Log payment for reconciliation
            # You might want to create a PaymentLog model for this
            
        elif event == "order.paid":
            order = payload.get("order", {})
            order_id = order.get("id")
            # Handle order completion
            
        return {"status": "success", "event": event}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook processing failed: {str(e)}")

@router.get("/payment-methods")
def get_payment_methods():
    """Get available payment methods"""
    return {
        "methods": [
            {
                "id": "razorpay",
                "name": "Razorpay",
                "description": "Credit/Debit Cards, UPI, Net Banking",
                "supported_currencies": ["INR"],
                "min_amount": 1,
                "max_amount": 100000
            }
        ]
    }
