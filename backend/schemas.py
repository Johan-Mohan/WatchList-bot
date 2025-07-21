# backend/schemas.py

from pydantic import BaseModel
from typing import Optional, List as PyList

# Movie Schemas
class MovieBase(BaseModel):
    tmdb_id: int
    title: str
    poster_path: Optional[str] = None
    release_date: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True

# ListMovie Schemas
class ListMovieBase(BaseModel):
    list_id: int
    movie_id: int
    user_rating: Optional[int] = None
    user_comment: Optional[str] = None

class ListMovieCreate(ListMovieBase):
    pass

class ListMovie(ListMovieBase):
    id: int
    movie: Movie

    class Config:
        orm_mode = True

# List Schemas
class ListBase(BaseModel):
    name: str
    user_id: int

class ListCreate(ListBase):
    pass

class List(ListBase):
    id: int
    is_watched_list: bool
    movies: PyList[ListMovie] = []

    class Config:
        orm_mode = True

# User Schemas
class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    lists: PyList[List] = []

    class Config:
        orm_mode = True
