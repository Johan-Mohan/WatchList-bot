# backend/models.py

from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, Text, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    
    lists = relationship("List", back_populates="owner")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, unique=True, index=True, nullable=False)
    title = Column(String, index=True)
    poster_path = Column(String)
    release_date = Column(String)

class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_watched_list = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="lists")
    movies = relationship("ListMovie", back_populates="list")

class ListMovie(Base):
    __tablename__ = "list_movies"

    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey("lists.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    user_rating = Column(Integer, nullable=True)
    user_comment = Column(Text, nullable=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    list = relationship("List", back_populates="movies")
    movie = relationship("Movie")

class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"))
    following_id = Column(Integer, ForeignKey("users.id"))
