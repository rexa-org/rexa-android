from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models
from ..db import get_db
from ..utils.auth_middleware import get_current_user_dependency

router = APIRouter()

@router.get("/", response_model=List[schemas.RewardOut])
def list_rewards(current_user: models.User = Depends(get_current_user_dependency), db: Session = Depends(get_db)):
    """Get all rewards for the current user"""
    return db.query(models.Reward).filter(models.Reward.owner_id == current_user.id).all()

@router.post("/", response_model=schemas.RewardOut)
def create_reward(reward: schemas.RewardCreate, current_user: models.User = Depends(get_current_user_dependency), db: Session = Depends(get_db)):
    """Create a new reward for the current user"""
    new_reward = models.Reward(**reward.dict(), owner_id=current_user.id)
    db.add(new_reward)
    db.commit()
    db.refresh(new_reward)
    return new_reward

@router.get("/{reward_id}", response_model=schemas.RewardOut)
def get_reward(reward_id: int, current_user: models.User = Depends(get_current_user_dependency), db: Session = Depends(get_db)):
    """Get a specific reward by ID"""
    db_reward = db.query(models.Reward).filter(
        models.Reward.id == reward_id, 
        models.Reward.owner_id == current_user.id
    ).first()
    if not db_reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    return db_reward

@router.put("/{reward_id}", response_model=schemas.RewardOut)
def update_reward(reward_id: int, reward: schemas.RewardCreate, current_user: models.User = Depends(get_current_user_dependency), db: Session = Depends(get_db)):
    """Update a reward"""
    db_reward = db.query(models.Reward).filter(
        models.Reward.id == reward_id, 
        models.Reward.owner_id == current_user.id
    ).first()
    if not db_reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    
    for key, value in reward.dict().items():
        setattr(db_reward, key, value)
    
    db.commit()
    db.refresh(db_reward)
    return db_reward

@router.delete("/{reward_id}")
def delete_reward(reward_id: int, current_user: models.User = Depends(get_current_user_dependency), db: Session = Depends(get_db)):
    """Delete a reward"""
    db_reward = db.query(models.Reward).filter(
        models.Reward.id == reward_id, 
        models.Reward.owner_id == current_user.id
    ).first()
    if not db_reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    
    db.delete(db_reward)
    db.commit()
    return {"message": "Reward deleted successfully"}

@router.post("/{reward_id}/list")
def list_reward_for_sale(reward_id: int, listing: schemas.ListingBase, current_user: models.User = Depends(get_current_user_dependency), db: Session = Depends(get_db)):
    """List a reward for sale in the marketplace"""
    db_reward = db.query(models.Reward).filter(
        models.Reward.id == reward_id, 
        models.Reward.owner_id == current_user.id
    ).first()
    if not db_reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    
    if db_reward.is_listed:
        raise HTTPException(status_code=400, detail="Reward is already listed")
    
    new_listing = models.Listing(**listing.dict())
    db.add(new_listing)
    db_reward.is_listed = True
    db.commit()
    db.refresh(new_listing)
    return {"message": "Reward listed successfully", "listing_id": new_listing.id}
