-- SQLite schema for recipes
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    cuisine TEXT,
    country_state TEXT,
    continent TEXT,
    url TEXT,
    rating REAL,
    total_time INTEGER,
    prep_time INTEGER,
    cook_time INTEGER,
    serves TEXT,
    description TEXT,

    -- nutrients (numeric, nullable)
    calories_kcal REAL,
    carbohydrate_g REAL,
    cholesterol_mg REAL,
    fiber_g REAL,
    protein_g REAL,
    saturated_fat_g REAL,
    sodium_mg REAL,
    sugar_g REAL,
    fat_g REAL,
    unsaturated_fat_g REAL,

    -- raw text blobs
    ingredients TEXT,     -- JSON string array
    instructions TEXT     -- JSON string array
);

CREATE INDEX IF NOT EXISTS idx_recipes_rating ON recipes(rating DESC);
CREATE INDEX IF NOT EXISTS idx_recipes_total_time ON recipes(total_time);
CREATE INDEX IF NOT EXISTS idx_recipes_title ON recipes(title);
CREATE INDEX IF NOT EXISTS idx_recipes_cuisine ON recipes(cuisine);
