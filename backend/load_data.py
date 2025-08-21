import json, sqlite3, re, math
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "recipes.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "models.sql"
DATA_JSON = Path(__file__).resolve().parents[1] / "data" / "US_recipes.json"

def to_number(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        if math.isnan(val):  # handle NaN floats
            return None
        return float(val)
    s = str(val).strip()
    if s.lower() == "nan" or s == "":
        return None
    # Extract first numeric (int/float) in the string, e.g., "389 kcal", "48 g"
    m = re.search(r'[-+]?\d*\.?\d+', s)
    return float(m.group()) if m else None

def clean_text(s):
    if s is None:
        return None
    s = str(s).strip()
    return s if s else None

def main():
    if not DATA_JSON.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_JSON}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # apply schema
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cur.executescript(f.read())

    # read JSON as object mapping (the provided file is an object with numbered keys)
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for _, rec in data.items():
        nutrients = rec.get("nutrients") or {}
        row = (
            clean_text(rec.get("title")),
            clean_text(rec.get("cuisine")),
            clean_text(rec.get("Country_State")),
            clean_text(rec.get("Contient")),
            clean_text(rec.get("URL")),
            to_number(rec.get("rating")),
            to_number(rec.get("total_time")),
            to_number(rec.get("prep_time")),
            to_number(rec.get("cook_time")),
            clean_text(rec.get("serves")),
            clean_text(rec.get("description")),

            to_number(nutrients.get("calories")),
            to_number(nutrients.get("carbohydrateContent")),
            to_number(nutrients.get("cholesterolContent")),
            to_number(nutrients.get("fiberContent")),
            to_number(nutrients.get("proteinContent")),
            to_number(nutrients.get("saturatedFatContent")),
            to_number(nutrients.get("sodiumContent")),
            to_number(nutrients.get("sugarContent")),
            to_number(nutrients.get("fatContent")),
            to_number(nutrients.get("unsaturatedFatContent")),

            json.dumps(rec.get("ingredients") or [], ensure_ascii=False),
            json.dumps(rec.get("instructions") or [], ensure_ascii=False),
        )
        rows.append(row)

    cur.execute("DELETE FROM recipes")
    cur.executemany(
        """
        INSERT INTO recipes (
            title, cuisine, country_state, continent, url, rating, total_time, prep_time, cook_time, serves, description,
            calories_kcal, carbohydrate_g, cholesterol_mg, fiber_g, protein_g, saturated_fat_g, sodium_mg, sugar_g, fat_g, unsaturated_fat_g,
            ingredients, instructions
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, ?,?)
        """,
        rows
    )
    conn.commit()
    conn.close()
    print(f"Loaded {len(rows)} records into {DB_PATH}")

if __name__ == "__main__":
    main()
