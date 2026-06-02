-- create_star_schema.sql
-- Federal Spending Anomaly Detection
-- Phase 3, Step 14: star schema (curated dimensional model)
-- Author: Hari Acharya
-- Source table: stg_awards_clean (16,866 rows)
--
-- Design notes:
--   Grain of fact_award is one row per unique award (generated_internal_id).
--   No agency dimension: every award is NASA, so a one row table adds nothing.
--   Two date foreign keys (start and end), because the dataset is awards
--     active during FY2022 and FY2023, so both ends of the period matter.
--   risk_score is created now with a default of 0 and is filled in Phase 4.

-- Drop in dependency order so the script can be run again cleanly.
DROP TABLE IF EXISTS fact_award;
DROP TABLE IF EXISTS dim_recipient;
DROP TABLE IF EXISTS dim_naics;
DROP TABLE IF EXISTS dim_psc;
DROP TABLE IF EXISTS dim_date;

-- Recipient dimension: the distinct vendors (about 4,064).
CREATE TABLE dim_recipient (
    recipient_key   SERIAL PRIMARY KEY,
    recipient_name  TEXT NOT NULL UNIQUE
);

-- NAICS dimension: industry code and its description (about 412 codes).
CREATE TABLE dim_naics (
    naics_key          SERIAL PRIMARY KEY,
    naics_code         TEXT NOT NULL UNIQUE,
    naics_description  TEXT
);

-- PSC dimension: product or service code and its description (about 779 codes).
CREATE TABLE dim_psc (
    psc_key          SERIAL PRIMARY KEY,
    psc_code         TEXT NOT NULL UNIQUE,
    psc_description  TEXT
);

-- Date dimension: one row per calendar day in the data span.
-- date_key is the date written as an integer in YYYYMMDD form,
-- which keeps joins simple and the load deterministic.
CREATE TABLE dim_date (
    date_key        INTEGER PRIMARY KEY,   -- e.g. 20221001
    full_date       DATE NOT NULL UNIQUE,
    year            INTEGER NOT NULL,
    quarter         INTEGER NOT NULL,      -- calendar quarter 1 to 4
    month           INTEGER NOT NULL,      -- 1 to 12
    fiscal_year     INTEGER NOT NULL,      -- federal FY, starts 1 October
    fiscal_quarter  INTEGER NOT NULL       -- federal FY quarter 1 to 4
);

-- Fact table: one row per unique award.
CREATE TABLE fact_award (
    award_sk               SERIAL PRIMARY KEY,
    generated_internal_id  TEXT NOT NULL UNIQUE,    -- natural key from the API
    award_id               TEXT,
    recipient_key          INTEGER REFERENCES dim_recipient (recipient_key),
    naics_key              INTEGER REFERENCES dim_naics (naics_key),
    psc_key                INTEGER REFERENCES dim_psc (psc_key),
    start_date_key         INTEGER REFERENCES dim_date (date_key),
    end_date_key           INTEGER REFERENCES dim_date (date_key),
    award_amount           NUMERIC(18,2),           -- the measure, in dollars
    risk_score             NUMERIC(10,2) DEFAULT 0  -- filled in Phase 4
);

-- Helpful indexes for the joins the rules and dashboards will use.
CREATE INDEX idx_fact_recipient  ON fact_award (recipient_key);
CREATE INDEX idx_fact_naics      ON fact_award (naics_key);
CREATE INDEX idx_fact_psc        ON fact_award (psc_key);
CREATE INDEX idx_fact_start_date ON fact_award (start_date_key);
CREATE INDEX idx_fact_end_date   ON fact_award (end_date_key);
