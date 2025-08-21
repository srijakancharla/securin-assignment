# Securin Assignment – Recipes Full-Stack

This package contains:

- **Backend:** FastAPI + SQLite with endpoints:
  - `GET /api/recipes?page=&limit=&sort=`
  - `GET /api/recipes/search?title=&cuisine=&rating_min=&rating_max=&calories_max=&total_time_max=&page=&limit=&sort=`
- **Data loader:** parses `data/US_recipes.json`, handles NaN/strings like `"389 kcal"` → `389.0`, and inserts into SQLite.
- **Frontend:** Simple Tailwind+JS table with filters (title, cuisine, max total time, max calories, min rating), pagination (15/20/30/50), star rating, serves, and a details drawer.

## Quick Start

### 1) Backend
```bash
cd backend
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python load_data.py                   # builds recipes.db and loads data
uvicorn app:app --reload --port 8000
```

### 2) Frontend
Open `frontend/index.html` in your browser (or serve with any static server).  
It fetches from `http://127.0.0.1:8000`.

> If you run backend on a different host/port, update `frontend/script.js` constant `API` base URL.

## SQL Schema
See `backend/models.sql`.

## Notes
- Sorting options: `rating_desc`, `rating_asc`, `time_asc`, `time_desc`.
- Null-safe filters: calories/time allow NULL values but filter upper-bounds when present.
- CORS enabled for simplicity.

## What to Submit
- Zip this whole folder **or** push to a public repo and share the link.
