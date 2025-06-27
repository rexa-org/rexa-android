from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..db import get_db
from ..utils.jwt_utils import decode_token

router = APIRouter()

def admin_required(token: str):
    payload = decode_token(token)
    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return payload

@router.get("/commission-report")
def commission_report(token: str, db: Session = Depends(get_db)):
    admin_required(token)
    logs = db.query(models.CommissionLog).all()
    total = sum([float(l.amount) for l in logs])
    return {"total_commission": total, "logs": logs}

@router.get("/moderation-queue")
def moderation_queue(token: str, db: Session = Depends(get_db)):
    admin_required(token)
    rewards = db.query(models.Reward).filter(models.Reward.is_listed == True).all()
    return rewards
