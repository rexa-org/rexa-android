from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..db import get_db
from ..utils.jwt_utils import decode_token

router = APIRouter()

@router.get("/", response_model=schemas.WalletOut)
def get_wallet(token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == payload["user_id"]).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@router.post("/deposit")
def deposit(token: str, amount: float, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == payload["user_id"]).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    wallet.money += amount
    db.commit()
    return {"ok": True, "money": float(wallet.money)}

@router.post("/withdraw")
def withdraw(token: str, amount: float, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == payload["user_id"]).first()
    if not wallet or wallet.money < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    wallet.money -= amount
    db.commit()
    return {"ok": True, "money": float(wallet.money)}
