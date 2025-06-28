from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models
from ..db import get_db
from ..utils.auth_middleware import get_current_user_dependency

router = APIRouter()

@router.get("/", response_model=schemas.WalletOut)
def get_wallet(current_user: models.User = Depends(get_current_user_dependency), db: Session = Depends(get_db)):
    """Get current user's wallet"""
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if not wallet:
        # Create wallet if it doesn't exist
        wallet = models.Wallet(user_id=current_user.id)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet

@router.post("/deposit")
def deposit(amount: float, current_user: models.User = Depends(get_current_user_dependency), db: Session = Depends(get_db)):
    """Deposit money into wallet"""
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if not wallet:
        wallet = models.Wallet(user_id=current_user.id, money=amount)
        db.add(wallet)
    else:
    wallet.money += amount
    
    db.commit()
    db.refresh(wallet)
    return {"message": "Deposit successful", "balance": float(wallet.money)}

@router.post("/withdraw")
def withdraw(amount: float, current_user: models.User = Depends(get_current_user_dependency), db: Session = Depends(get_db)):
    """Withdraw money from wallet"""
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if not wallet or wallet.money < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    wallet.money -= amount
    db.commit()
    db.refresh(wallet)
    return {"message": "Withdrawal successful", "balance": float(wallet.money)}

@router.get("/transactions", response_model=List[schemas.TransactionOut])
def get_transactions(current_user: models.User = Depends(get_current_user_dependency), db: Session = Depends(get_db)):
    """Get user's transaction history"""
    transactions = db.query(models.Transaction).filter(
        models.Transaction.buyer_id == current_user.id
    ).order_by(models.Transaction.created_at.desc()).all()
    return transactions

@router.post("/add-points")
def add_points(points: int, current_user: models.User = Depends(get_current_user_dependency), db: Session = Depends(get_db)):
    """Add points to wallet (for rewards, etc.)"""
    if points <= 0:
        raise HTTPException(status_code=400, detail="Points must be positive")
    
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if not wallet:
        wallet = models.Wallet(user_id=current_user.id, points=points)
        db.add(wallet)
    else:
        wallet.points += points
    
    db.commit()
    db.refresh(wallet)
    return {"message": "Points added successfully", "points": wallet.points}
