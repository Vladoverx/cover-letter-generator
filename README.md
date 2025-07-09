# CV Generator

A full-stack application for generating CVs and cover letters using AI.

## Features

- Create and manage CV profiles
- Generate AI-powered cover letters using Google's Gemini LLM
- RESTful API with FastAPI backend
- Modern frontend interface

## Prerequisites

- Google AI API key
- Python 3.11
- uv (package manager)

## Setup

1. Clone the repository
2. Install dependencies: `uv sync`
3. Set up environment variables inside the `backend/.env` file
4. Run the application: `uv run backend/run.py`
5. Run the frontend

## API Endpoints

### Cover Letters

- `POST /api/v1/cover-letters/generate` - Generate a cover letter using AI
- `GET /api/v1/cover-letters/user/{user_id}` - Get user's cover letters
- `GET /api/v1/cover-letters/{cover_letter_id}` - Get specific cover letter
- `PUT /api/v1/cover-letters/{cover_letter_id}` - Update cover letter
- `DELETE /api/v1/cover-letters/{cover_letter_id}` - Delete cover letter

### Users and CVs

- See API documentation at `http://localhost:8000/docs` when running

## Architecture

- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: SQLite
- **AI Integration**: Google Gemini 2.5 Flash for cover letter generation
- **Frontend**: JavaScript with modern components

## Development

The application follows clean architecture principles:

- `models/` - Database models
- `schemas/` - Pydantic schemas for API
- `services/` - Business logic layer
- `api/routes/` - API route handlers
- `core/` - Configuration and dependencies

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google AI API key for cover letter generation | Yes |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |
| `ALLOWED_HOSTS` | CORS allowed origins | No |


## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── cover_letter_routes.py
│   │   │   ├── cv_routes.py
│   │   │   ├── user_routes.py
│   │   │   └── __init__.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── dependencies.py
│   │   │   ├── init_db.py
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   ├── cover_letter.py
│   │   │   ├── cv_profile.py
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   ├── cover_letter.py
│   │   │   ├── cv_profile.py
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── cover_letter_service.py
│   │   │   ├── cv_service.py
│   │   │   ├── user_service.py
│   │   │   └── __init__.py
│   ├── __init__.py
│   └── main.py
├── run.py
└── .env
frontend/
├── js/
│   ├── services/
│   │   └── apiService.js          # API communication layer
│   ├── state/
│   │   └── appState.js            # Centralized state management
│   ├── utils/
│   │   └── helpers.js             # Utility functions
│   ├── components/
│   │   ├── authComponent.js       # Authentication logic
│   │   ├── navigationComponent.js # Navigation management
│   │   ├── profileComponent.js    # Profile form handling
│   │   └── coverLetterComponent.js # Cover letter operations
│   └── app.js                     # Main application coordinator
├── index.html                     # Main HTML file
├── styles.css                     # Styles
```