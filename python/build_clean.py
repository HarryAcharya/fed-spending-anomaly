"""
build_clean.py
Phase 3 (cleaning). Build a clean, analysis-ready table from staging.

It reads stg_awards_raw from PostgreSQL, then:
  - parses the NAICS and PSC bundles into separate code and description columns
  - standardizes recipient names (trim, collapse repeated spaces, uppercase)
  - converts award_amount from text into a real number
  - converts start_date and end_date from text into real dates
  - keeps only the columns we need downstream and drops the empty award_type
It writes the result to stg_awards_clean. The raw staging table is not changed.

Run from the project folder with the venv active:
    python python/build_clean.py
"""

import os
import re
import ast
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "fed_spending")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")

url = (
    f"postgresql+psycopg2://{DB_USER}:{quote_plus(DB_PASSWORD)}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine = create_engine(url)

SOURCE_TABLE = "stg_awards_raw"
CLEAN_TABLE = "stg_awards_clean"


def parse_bundle(value):
    """
    Turn a stored bundle like
        {'code': '541712', 'description': 'RESEARCH AND ...'}
    into a (code, description) pair. Returns (None, None) if the value is
    missing or cannot be read.
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None, None
    text = str(value).strip()
    if not text.startswith("{"):
        return None, None
    try:
        bundle = ast.literal_eval(text)
        return bundle.get("code"), bundle.get("description")
    except (ValueError, SyntaxError):
        return None, None


def clean_name(value):
    """Trim, collapse repeated spaces, and uppercase a recipient name."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = re.sub(r"\s+", " ", str(value).strip()).upper()
    return text if text else None


print("Reading", SOURCE_TABLE, "from the database...")
df = pd.read_sql_table(SOURCE_TABLE, engine)
print("  ", len(df), "rows read")

print("Parsing NAICS and PSC bundles into code and description...")
df["naics_code"], df["naics_description"] = zip(*df["naics"].map(parse_bundle))
df["psc_code"], df["psc_description"] = zip(*df["psc"].map(parse_bundle))

print("Standardizing recipient names...")
df["recipient_name"] = df["recipient_name"].map(clean_name)

print("Converting amount and dates to proper types...")
df["award_amount"] = pd.to_numeric(df["award_amount"], errors="coerce")
df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce").dt.date
df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce").dt.date

# Keep only the columns we need downstream, in a sensible order.
clean = df[[
    "generated_internal_id",
    "award_id",
    "recipient_name",
    "award_amount",
    "start_date",
    "end_date",
    "naics_code",
    "naics_description",
    "psc_code",
    "psc_description",
]].copy()

print("Writing", CLEAN_TABLE, "to the database...")
clean.to_sql(CLEAN_TABLE, engine, if_exists="replace", index=False)
print("  wrote", len(clean), "rows")

print()
print("Summary of the clean table:")
print("  rows:", len(clean))
print("  unique recipients:", clean["recipient_name"].nunique())
print("  unique NAICS codes:", clean["naics_code"].nunique())
print("  unique PSC codes:", clean["psc_code"].nunique())
print("  amounts that could not be parsed:", int(clean["award_amount"].isna().sum()))
print("  start dates that could not be parsed:", int(clean["start_date"].isna().sum()))
print("  end dates that could not be parsed:", int(clean["end_date"].isna().sum()))
print()
print("Done. The raw staging table was not changed.")
