# backend/routers/lists.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.List)
def create_list(list_data: schemas.ListCreate, db: Session = Depends(get_db)):
    """
    Create a new custom list for a user.
    """
    db_user = db.query(models.User).filter(models.User.id == list_data.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    new_list = models.List(name=list_data.name, user_id=list_data.user_id)
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list

@router.post("/movies", response_model=schemas.ListMovie)
def add_movie_to_list(item: schemas.ListMovieCreate, db: Session = Depends(get_db)):
    """
    Add a movie to a list.
    """
    db_list = db.query(models.List).filter(models.List.id == item.list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
        
    db_movie = db.query(models.Movie).filter(models.Movie.id == item.movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Check if movie is already in the list
    existing_entry = db.query(models.ListMovie).filter_by(list_id=item.list_id, movie_id=item.movie_id).first()
    if existing_entry:
        raise HTTPException(status_code=400, detail="Movie already in this list")

    new_list_movie = models.ListMovie(**item.dict())
    db.add(new_list_movie)
    db.commit()
    db.refresh(new_list_movie)
    return new_list_movie
