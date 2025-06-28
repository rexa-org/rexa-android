from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from .. import schemas, models
from ..db import get_db
from ..utils.auth_middleware import get_current_admin_user

router = APIRouter()

@router.get("/commission-report")
def commission_report(current_user: models.User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    """Get commission report for admin"""
    # Get total commission
    total_commission = db.query(func.sum(models.CommissionLog.amount)).scalar() or 0
    
    # Get recent commission logs
    recent_logs = db.query(models.CommissionLog).order_by(
        models.CommissionLog.created_at.desc()
    ).limit(50).all()
    
    # Get commission by month
    monthly_commission = db.query(
        func.date_trunc('month', models.CommissionLog.created_at).label('month'),
        func.sum(models.CommissionLog.amount).label('total')
    ).group_by('month').order_by('month').all()
    
    return {
        "total_commission": float(total_commission),
        "recent_logs": recent_logs,
        "monthly_breakdown": [
            {"month": str(log.month), "total": float(log.total)} 
            for log in monthly_commission
        ]
    }

@router.get("/moderation-queue")
def moderation_queue(current_user: models.User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    """Get rewards pending moderation"""
    pending_rewards = db.query(models.Reward).filter(
        models.Reward.is_listed == True
    ).all()
    return pending_rewards

@router.post("/rewards/{reward_id}/approve")
def approve_reward(reward_id: int, current_user: models.User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    """Approve a reward listing"""
    reward = db.query(models.Reward).filter(models.Reward.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    
    # Add approval logic here if needed
    db.commit()
    return {"message": "Reward approved successfully"}

@router.post("/rewards/{reward_id}/reject")
def reject_reward(reward_id: int, reason: str, current_user: models.User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    """Reject a reward listing"""
    reward = db.query(models.Reward).filter(models.Reward.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    
    # Mark as not listed
    reward.is_listed = False
    db.commit()
    return {"message": "Reward rejected", "reason": reason}

@router.get("/users", response_model=List[schemas.UserOut])
def list_users(current_user: models.User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    """Get all users (admin only)"""
    users = db.query(models.User).all()
    return users

@router.get("/statistics")
def get_statistics(current_user: models.User = Depends(get_current_admin_user), db: Session = Depends(get_db)):
    """Get platform statistics"""
    total_users = db.query(models.User).count()
    total_rewards = db.query(models.Reward).count()
    total_transactions = db.query(models.Transaction).count()
    total_commission = db.query(func.sum(models.CommissionLog.amount)).scalar() or 0
    
    return {
        "total_users": total_users,
        "total_rewards": total_rewards,
        "total_transactions": total_transactions,
        "total_commission": float(total_commission)
    }
