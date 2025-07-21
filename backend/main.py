# backend/main.py

from fastapi import FastAPI
from .database import engine, Base
from .routers import users, movies, lists

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Telegram Movie Tracker API",
    description="API for the Telegram Movie Tracker Mini App.",
    version="0.1.0",
)

# Include the API routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(movies.router, prefix="/api/movies", tags=["movies"])
app.include_router(lists.router, prefix="/api/lists", tags=["lists"])

@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Movie Tracker API!"}
