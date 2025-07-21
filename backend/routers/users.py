# backend/routers/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    db_user = db.query(models.User).filter(models.User.telegram_id == user.telegram_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User with this Telegram ID already registered")
    
    new_user = models.User(telegram_id=user.telegram_id, username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Also create a default "Watched" list for the new user
    watched_list = models.List(name="Watched", is_watched_list=True, user_id=new_user.id)
    db.add(watched_list)
    db.commit()
    
    return new_user

@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by their ID.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
