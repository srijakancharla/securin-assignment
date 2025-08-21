from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3, math
from typing import Optional, List, Literal, Tuple

DB_PATH = "recipes.db"

app = FastAPI(title="Securin Recipes API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Recipe(BaseModel):
    id: int
    title: str
    cuisine: Optional[str] = None
    country_state: Optional[str] = None
    continent: Optional[str] = None
    url: Optional[str] = None
    rating: Optional[float] = None
    total_time: Optional[int] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    serves: Optional[str] = None
    description: Optional[str] = None
    calories_kcal: Optional[float] = None
    carbohydrate_g: Optional[float] = None
    cholesterol_mg: Optional[float] = None
    fiber_g: Optional[float] = None
    protein_g: Optional[float] = None
    saturated_fat_g: Optional[float] = None
    sodium_mg: Optional[float] = None
    sugar_g: Optional[float] = None
    fat_g: Optional[float] = None
    unsaturated_fat_g: Optional[float] = None
    ingredients: Optional[str] = None
    instructions: Optional[str] = None

def count_where(cur, where: str, params: Tuple):
    sql = f"SELECT COUNT(*) AS c FROM recipes {where}"
    cur.execute(sql, params)
    return cur.fetchone()["c"]

@app.get("/api/recipes")
def list_recipes(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: Literal["rating_desc","rating_asc","time_asc","time_desc"] = "rating_desc",
):
    sort_map = {
        "rating_desc": "rating DESC NULLS LAST",
        "rating_asc": "rating ASC NULLS LAST",
        "time_asc": "total_time ASC NULLS LAST",
        "time_desc": "total_time DESC NULLS LAST",
    }
    order_by = sort_map.get(sort, "rating DESC")
    offset = (page - 1) * limit

    conn = get_db()
    cur = conn.cursor()
    total = count_where(cur, " ", ())
    cur.execute(f"SELECT * FROM recipes ORDER BY {order_by} LIMIT ? OFFSET ?", (limit, offset))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {"page": page, "limit": limit, "total": total, "data": rows}

@app.get("/api/recipes/search")
def search_recipes(
    title: Optional[str] = None,
    cuisine: Optional[str] = None,
    rating_min: Optional[float] = Query(None, ge=0, le=5),
    rating_max: Optional[float] = Query(None, ge=0, le=5),
    calories_max: Optional[float] = None,
    total_time_max: Optional[int] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: Literal["rating_desc","rating_asc","time_asc","time_desc"] = "rating_desc",
):
    clauses = []
    params = []

    if title:
        clauses.append("LOWER(title) LIKE ?")
        params.append(f"%{title.lower()}%")
    if cuisine:
        clauses.append("LOWER(cuisine) LIKE ?")
        params.append(f"%{cuisine.lower()}%")
    if rating_min is not None:
        clauses.append("rating >= ?")
        params.append(rating_min)
    if rating_max is not None:
        clauses.append("rating <= ?")
        params.append(rating_max)
    if calories_max is not None:
        clauses.append("(calories_kcal IS NULL OR calories_kcal <= ?)")
        params.append(calories_max)
    if total_time_max is not None:
        clauses.append("(total_time IS NULL OR total_time <= ?)")
        params.append(total_time_max)

    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    sort_map = {
        "rating_desc": "rating DESC NULLS LAST",
        "rating_asc": "rating ASC NULLS LAST",
        "time_asc": "total_time ASC NULLS LAST",
        "time_desc": "total_time DESC NULLS LAST",
    }
    order_by = sort_map.get(sort, "rating DESC")
    offset = (page - 1) * limit

    conn = get_db()
    cur = conn.cursor()
    total = count_where(cur, where, tuple(params))
    cur.execute(f"SELECT * FROM recipes {where} ORDER BY {order_by} LIMIT ? OFFSET ?", (*params, limit, offset))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {"page": page, "limit": limit, "total": total, "data": rows}
