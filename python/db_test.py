"""
db_test.py
Phase 3. A single test connection to PostgreSQL.

Purpose: confirm we can reach the database before we build any tables.
It reads the connection settings from the .env file, connects, and asks
PostgreSQL for its version. Nothing is created or changed.

Run from the project folder with the venv active:
    python python/db_test.py
"""

import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load the settings from the .env file into the environment.
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "fed_spending")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if not DB_PASSWORD or DB_PASSWORD == "PUT_YOUR_PASSWORD_HERE":
    print("No real password found in .env.")
    print("Open the .env file and set DB_PASSWORD to your PostgreSQL password.")
    raise SystemExit(1)

# Build the connection string. The password is URL encoded in case it
# contains characters like @ or # that would otherwise break the string.
url = (
    f"postgresql+psycopg2://{DB_USER}:{quote_plus(DB_PASSWORD)}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("Connecting to PostgreSQL...")
print("  host:", DB_HOST, "port:", DB_PORT, "database:", DB_NAME, "user:", DB_USER)

try:
    engine = create_engine(url)
    with engine.connect() as connection:
        version = connection.execute(text("SELECT version();")).scalar()
        print("Connected successfully.")
        print("PostgreSQL says:", version)
except Exception as error:
    print("Could not connect.")
    print("Error:", error)
    raise SystemExit(1)

print("Test complete.")
