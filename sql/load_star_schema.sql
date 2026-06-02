-- load_star_schema.sql
-- Federal Spending Anomaly Detection
-- Phase 3, Step 15: load the star schema from stg_awards_clean
-- Author: Hari Acharya
--
-- Order matters: load the dimensions first so the fact can look up their
-- surrogate keys. The script is safe to run again because it truncates the
-- tables first and resets the surrogate key counters.

-- Clear the model and reset the SERIAL counters so a reload starts fresh.
TRUNCATE fact_award, dim_recipient, dim_naics, dim_psc, dim_date RESTART IDENTITY;

-- 1. Recipient dimension: one row per distinct vendor name.
INSERT INTO dim_recipient (recipient_name)
SELECT DISTINCT recipient_name
FROM stg_awards_clean
WHERE recipient_name IS NOT NULL AND recipient_name <> ''
ORDER BY recipient_name;

-- 2. NAICS dimension: one row per code, keeping a single description per code.
INSERT INTO dim_naics (naics_code, naics_description)
SELECT naics_code, MAX(naics_description)
FROM stg_awards_clean
WHERE naics_code IS NOT NULL AND naics_code <> ''
GROUP BY naics_code
ORDER BY naics_code;

-- 3. PSC dimension: one row per code, keeping a single description per code.
INSERT INTO dim_psc (psc_code, psc_description)
SELECT psc_code, MAX(psc_description)
FROM stg_awards_clean
WHERE psc_code IS NOT NULL AND psc_code <> ''
GROUP BY psc_code
ORDER BY psc_code;

-- 4. Date dimension: one row per distinct day seen in either date column.
--    date_key is the date as an integer in YYYYMMDD form.
--    Federal fiscal year starts on 1 October.
INSERT INTO dim_date (date_key, full_date, year, quarter, month, fiscal_year, fiscal_quarter)
SELECT
    to_char(d, 'YYYYMMDD')::int            AS date_key,
    d                                      AS full_date,
    EXTRACT(YEAR  FROM d)::int             AS year,
    EXTRACT(QUARTER FROM d)::int           AS quarter,
    EXTRACT(MONTH FROM d)::int             AS month,
    CASE WHEN EXTRACT(MONTH FROM d) >= 10
         THEN EXTRACT(YEAR FROM d)::int + 1
         ELSE EXTRACT(YEAR FROM d)::int
    END                                    AS fiscal_year,
    CASE
         WHEN EXTRACT(MONTH FROM d) IN (10, 11, 12) THEN 1
         WHEN EXTRACT(MONTH FROM d) IN (1, 2, 3)    THEN 2
         WHEN EXTRACT(MONTH FROM d) IN (4, 5, 6)    THEN 3
         ELSE 4
    END                                    AS fiscal_quarter
FROM (
    SELECT start_date AS d FROM stg_awards_clean WHERE start_date IS NOT NULL
    UNION
    SELECT end_date        FROM stg_awards_clean WHERE end_date   IS NOT NULL
) distinct_dates
ORDER BY d;

-- 5. Fact table: one row per award, joined to each dimension key.
--    LEFT JOINs are used so an award with a missing code or date still loads,
--    with that foreign key left empty rather than the row being dropped.
INSERT INTO fact_award (
    generated_internal_id, award_id,
    recipient_key, naics_key, psc_key,
    start_date_key, end_date_key,
    award_amount
)
SELECT
    c.generated_internal_id,
    c.award_id,
    r.recipient_key,
    n.naics_key,
    p.psc_key,
    sd.date_key,
    ed.date_key,
    c.award_amount::numeric(18,2)
FROM stg_awards_clean c
LEFT JOIN dim_recipient r  ON r.recipient_name = c.recipient_name
LEFT JOIN dim_naics     n  ON n.naics_code     = c.naics_code
LEFT JOIN dim_psc       p  ON p.psc_code       = c.psc_code
LEFT JOIN dim_date      sd ON sd.full_date     = c.start_date
LEFT JOIN dim_date      ed ON ed.full_date     = c.end_date;