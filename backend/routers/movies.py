# backend/routers/movies.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
import os
from .. import models, schemas
from ..database import get_db

router = APIRouter()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_API_URL = "https://api.themoviedb.org/3"

@router.get("/search", response_model=list[schemas.Movie])
def search_movies(query: str, db: Session = Depends(get_db)):
    """
    Search for movies on TMDB.
    """
    if not query:
        return []
        
    try:
        response = requests.get(
            f"{TMDB_API_URL}/search/movie",
            params={"api_key": TMDB_API_KEY, "query": query}
        )
        response.raise_for_status()
        data = response.json()

        movies = []
        for item in data.get("results", []):
            # Check if movie exists in our DB, if not, add it.
            db_movie = db.query(models.Movie).filter(models.Movie.tmdb_id == item['id']).first()
            if not db_movie:
                new_movie = models.Movie(
                    tmdb_id=item['id'],
                    title=item['title'],
                    poster_path=item.get('poster_path'),
                    release_date=item.get('release_date')
                )
                db.add(new_movie)
                db.commit()
                db.refresh(new_movie)
                movies.append(new_movie)
            else:
                movies.append(db_movie)
        
        return movies

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error contacting TMDB API: {e}")
