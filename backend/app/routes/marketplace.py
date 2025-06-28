from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .. import schemas, models
from ..db import get_db
from ..utils.auth_middleware import get_current_user_dependency

router = APIRouter()

@router.get("/", response_model=List[schemas.ListingOut])
def list_marketplace(
    type: Optional[str] = Query(None, description="Filter by listing type"),
    source: Optional[str] = Query(None, description="Filter by source app"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    db: Session = Depends(get_db)
):
    """Get all active marketplace listings with optional filters"""
    query = db.query(models.Listing).filter(models.Listing.is_active == True)
    
    if type:
        query = query.filter(models.Listing.type == type)
    if source:
        query = query.join(models.Reward).filter(models.Reward.source_app == source)
    if min_price is not None:
        query = query.filter(models.Listing.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Listing.price <= max_price)
    
    return query.all()

@router.get("/{listing_id}", response_model=schemas.ListingOut)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    """Get a specific marketplace listing"""
    listing = db.query(models.Listing).filter(
        models.Listing.id == listing_id,
        models.Listing.is_active == True
    ).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@router.post("/{listing_id}/buy")
def buy_reward(
    listing_id: int, 
    current_user: models.User = Depends(get_current_user_dependency), 
    db: Session = Depends(get_db)
):
    """Buy a reward from the marketplace"""
    listing = db.query(models.Listing).filter(
        models.Listing.id == listing_id,
        models.Listing.is_active == True
    ).first()
    
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    # Check if user is trying to buy their own listing
    reward = db.query(models.Reward).filter(models.Reward.id == listing.reward_id).first()
    if reward.owner_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot buy your own listing")
    
    # Calculate commission (1% of sale price)
    amount = float(listing.price)
    commission = round(amount * 0.01, 2)
    
    # Mark listing as inactive
    listing.is_active = False
    
    # Create transaction record
    transaction = models.Transaction(
        buyer_id=current_user.id,
        listing_id=listing.id,
        amount=amount,
        commission=commission
    )
    db.add(transaction)
    
    # Create commission log
    commission_log = models.CommissionLog(
        transaction_id=transaction.id,
        amount=commission
    )
    db.add(commission_log)
    
    # Update seller's wallet (transfer money to seller)
    seller_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == reward.owner_id).first()
    if seller_wallet:
        seller_wallet.money += (amount - commission)
    
    # Update buyer's wallet (deduct money from buyer)
    buyer_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if buyer_wallet:
        if buyer_wallet.money < amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        buyer_wallet.money -= amount
    
    # Transfer reward ownership
    reward.owner_id = current_user.id
    reward.is_listed = False
    
    db.commit()
    db.refresh(transaction)
    
    return {
        "message": "Purchase successful",
        "transaction_id": transaction.id,
        "amount": amount,
        "commission": commission
    }

@router.get("/search/", response_model=List[schemas.ListingOut])
def search_listings(
    q: str = Query(..., description="Search query"),
    db: Session = Depends(get_db)
):
    """Search marketplace listings by title or source app"""
    query = db.query(models.Listing).join(models.Reward).filter(
        models.Listing.is_active == True,
        (models.Reward.title.ilike(f"%{q}%") | models.Reward.source_app.ilike(f"%{q}%"))
    )
    return query.all()
