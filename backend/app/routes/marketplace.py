from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import schemas, models
from ..db import get_db
from ..utils.jwt_utils import decode_token

router = APIRouter()

@router.get("/", response_model=list[schemas.ListingOut])
def list_marketplace(type: str = None, source: str = None, price: float = None, expiry_before: str = None, db: Session = Depends(get_db)):
    q = db.query(models.Listing).filter(models.Listing.is_active == True)
    if type:
        q = q.filter(models.Listing.type == type)
    if source:
        q = q.join(models.Reward).filter(models.Reward.source_app == source)
    if price:
        q = q.filter(models.Listing.price <= price)
    # expiry_before is ISO string
    if expiry_before:
        from datetime import datetime
        q = q.join(models.Reward).filter(models.Reward.expiry < datetime.fromisoformat(expiry_before))
    return q.all()

@router.post("/{reward_id}/buy")
def buy_reward(reward_id: int, token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload["user_id"]
    listing = db.query(models.Listing).filter(models.Listing.reward_id == reward_id, models.Listing.is_active == True).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    # Deduct points or handle payment (stub)
    amount = float(listing.price)
    commission = round(amount * 0.01, 2)
    # Mark listing inactive
    listing.is_active = False
    db.commit()
    # Log transaction
    txn = models.Transaction(buyer_id=user_id, listing_id=listing.id, amount=amount, commission=commission)
    db.add(txn)
    db.commit()
    db.refresh(txn)
    # Log commission
    clog = models.CommissionLog(transaction_id=txn.id, amount=commission)
    db.add(clog)
    db.commit()
    return {"ok": True, "transaction_id": txn.id}
