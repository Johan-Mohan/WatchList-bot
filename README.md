# Telegram Movie Tracker Mini App

This project is a Telegram Mini App for tracking movies, creating watchlists, and sharing them with friends.

## Project Structure

- `backend/`: The Python FastAPI application that serves the API.
- `bot/`: The Python script for the Telegram bot.
- `frontend/`: The React-based web application for the user interface.
- `.env`: File for environment variables (you need to create this from `.env.example`).

## Setup and Installation

### 1. Prerequisites

- Python 3.8+
- Node.js and npm
- PostgreSQL
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- An API Key from [The Movie Database (TMDB)](https://www.themoviedb.org/documentation/api)

### 2. Environment Variables

- Copy the `.env.example` file to a new file named `.env`.
- Open the `.env` file and fill in your credentials for the Telegram bot, TMDB API, and your PostgreSQL database.

### 3. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn main:app --reload
```

### 4. Frontend Setup

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

### 5. Bot Setup

```bash
# Navigate to the bot directory
cd bot

# Make sure your backend virtual environment is activated
# or create a new one and install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

## How to Run

1.  Start your PostgreSQL server.
2.  Run the backend server.
3.  Run the frontend development server.
4.  Run the Telegram bot.
5.  Open Telegram and send the `/start` command to your bot. The menu button should appear, which will open the web app.
