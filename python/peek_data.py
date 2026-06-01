"""
peek_data.py
Phase 2, Step 11. Look at the raw data we pulled, before any cleaning.

This does not change anything. It just reads data/awards_raw.csv and prints
a summary so we understand what we are working with: the shape, the columns,
a few sample rows, where the gaps are, and some basic numbers.

Run from the project folder with the venv active:
    python python/peek_data.py
"""

import pandas as pd

INPUT_PATH = "data/awards_raw.csv"

# Show more columns and wider output so nothing is hidden.
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

df = pd.read_csv(INPUT_PATH)

print("=" * 70)
print("SHAPE")
print("=" * 70)
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print()

print("=" * 70)
print("COLUMNS AND TYPES")
print("=" * 70)
print(df.dtypes)
print()

print("=" * 70)
print("FIRST 5 ROWS")
print("=" * 70)
print(df.head())
print()

print("=" * 70)
print("MISSING VALUES PER COLUMN")
print("=" * 70)
missing = df.isna().sum()
for column, count in missing.items():
    pct = round(100 * count / len(df), 1)
    print(f"  {column:<28} {count:>8}  ({pct}%)")
print()

print("=" * 70)
print("AWARD AMOUNT SUMMARY")
print("=" * 70)
if "Award Amount" in df.columns:
    amounts = pd.to_numeric(df["Award Amount"], errors="coerce")
    print("  count of usable amounts:", int(amounts.notna().sum()))
    print("  minimum:", amounts.min())
    print("  maximum:", amounts.max())
    print("  average:", round(amounts.mean(), 2))
    print("  median:", amounts.median())
    print("  negative or zero amounts:", int((amounts <= 0).sum()))
print()

print("=" * 70)
print("A FEW USEFUL COUNTS")
print("=" * 70)
if "Recipient Name" in df.columns:
    print("  unique recipient names:", df["Recipient Name"].nunique())
if "Awarding Sub Agency" in df.columns:
    print("  unique awarding sub agencies:", df["Awarding Sub Agency"].nunique())
if "Start Date" in df.columns:
    dates = pd.to_datetime(df["Start Date"], errors="coerce")
    print("  earliest start date:", dates.min())
    print("  latest start date:", dates.max())
print()

print("Done. This was read only. Nothing was changed.")
