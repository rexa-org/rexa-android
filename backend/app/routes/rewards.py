from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..db import get_db
from ..utils.jwt_utils import decode_token

router = APIRouter()

@router.get("/", response_model=list[schemas.RewardOut])
def list_rewards(token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return db.query(models.Reward).filter(models.Reward.owner_id == payload["user_id"]).all()

@router.post("/", response_model=schemas.RewardOut)
def create_reward(reward: schemas.RewardCreate, token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    new_reward = models.Reward(**reward.dict(), owner_id=payload["user_id"])
    db.add(new_reward)
    db.commit()
    db.refresh(new_reward)
    return new_reward

@router.put("/{reward_id}", response_model=schemas.RewardOut)
def update_reward(reward_id: int, reward: schemas.RewardCreate, token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    db_reward = db.query(models.Reward).filter(models.Reward.id == reward_id, models.Reward.owner_id == payload["user_id"]).first()
    if not db_reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    for k, v in reward.dict().items():
        setattr(db_reward, k, v)
    db.commit()
    db.refresh(db_reward)
    return db_reward

@router.delete("/{reward_id}")
def delete_reward(reward_id: int, token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    db_reward = db.query(models.Reward).filter(models.Reward.id == reward_id, models.Reward.owner_id == payload["user_id"]).first()
    if not db_reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    db.delete(db_reward)
    db.commit()
    return {"ok": True}
