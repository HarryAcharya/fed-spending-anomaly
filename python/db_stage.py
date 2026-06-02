"""
db_stage.py
Phase 3. Load the raw CSV into a PostgreSQL staging table.

Purpose: create the "as received" layer (FR-02). Every row and column
from awards_raw.csv lands here unchanged. No cleaning, no type coercion.

Run from the project folder with the venv active:
    python python/db_stage.py
"""

import os
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "fed_spending")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if not DB_PASSWORD or DB_PASSWORD == "PUT_YOUR_PASSWORD_HERE":
    print("No real password found in .env.")
    raise SystemExit(1)

url = (
    f"postgresql+psycopg2://{DB_USER}:{quote_plus(DB_PASSWORD)}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(url)

# ---------------------------------------------------------------------------
# Load CSV
# ---------------------------------------------------------------------------
CSV_PATH = "data/awards_raw.csv"

print(f"Reading {CSV_PATH} ...")
df = pd.read_csv(CSV_PATH, dtype=str)
print(f"  {len(df)} rows, {len(df.columns)} columns")

# Normalise column names to lowercase with underscores for SQL.
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("-", "_", regex=False)
)

print("Columns after normalisation:")
for col in df.columns:
    print(f"  {col}")

# ---------------------------------------------------------------------------
# Write to staging table
# ---------------------------------------------------------------------------
TABLE = "stg_awards_raw"

print(f"\nWriting to table '{TABLE}' in database '{DB_NAME}' ...")

with engine.begin() as conn:
    # Drop and recreate so reruns are safe.
    conn.execute(text(f"DROP TABLE IF EXISTS {TABLE};"))

df.to_sql(TABLE, engine, if_exists="replace", index=False)

print(f"Done. {len(df)} rows loaded into {TABLE}.")

# ---------------------------------------------------------------------------
# Quick sanity check
# ---------------------------------------------------------------------------
with engine.connect() as conn:
    count = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE};")).scalar()
    print(f"Row count confirmed in PostgreSQL: {count}")

print("Staging load complete.")
