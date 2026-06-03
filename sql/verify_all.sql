-- verify_all.sql
-- Federal Spending Anomaly Detection
-- One stop verification. Re-derives every documented figure from the
-- live database and marks each PASS or FAIL against what we wrote in
-- the docs. Run with:
--   psql -U postgres -d fed_spending -f sql/verify_all.sql

\echo ''
\echo '================ SECTION 1: exact count checks (PASS/FAIL) ================'
WITH checks AS (
    SELECT 'stg_awards_raw rows'        AS check_name, 16866 AS expected, (SELECT count(*) FROM stg_awards_raw)::int                                AS actual
    UNION ALL SELECT 'stg_awards_clean rows',           16866, (SELECT count(*) FROM stg_awards_clean)::int
    UNION ALL SELECT 'fact_award rows',                 16866, (SELECT count(*) FROM fact_award)::int
    UNION ALL SELECT 'dim_recipient rows',               4064, (SELECT count(*) FROM dim_recipient)::int
    UNION ALL SELECT 'dim_naics rows',                    412, (SELECT count(*) FROM dim_naics)::int
    UNION ALL SELECT 'dim_psc rows',                      779, (SELECT count(*) FROM dim_psc)::int
    UNION ALL SELECT 'dim_date rows',                    3703, (SELECT count(*) FROM dim_date)::int
    UNION ALL SELECT 'missing recipient_key',               0, (SELECT count(*) FROM fact_award WHERE recipient_key IS NULL)::int
    UNION ALL SELECT 'missing naics_key',                   7, (SELECT count(*) FROM fact_award WHERE naics_key IS NULL)::int
    UNION ALL SELECT 'missing psc_key',                     0, (SELECT count(*) FROM fact_award WHERE psc_key IS NULL)::int
    UNION ALL SELECT 'missing start_date_key',              1, (SELECT count(*) FROM fact_award WHERE start_date_key IS NULL)::int
    UNION ALL SELECT 'missing end_date_key',                0, (SELECT count(*) FROM fact_award WHERE end_date_key IS NULL)::int
    UNION ALL SELECT 'R1 flagged',                        167, (SELECT count(*) FROM fact_award WHERE rule_r1 = 1)::int
    UNION ALL SELECT 'R2 flagged',                        291, (SELECT count(*) FROM fact_award WHERE rule_r2 = 1)::int
    UNION ALL SELECT 'R3 flagged',                        216, (SELECT count(*) FROM fact_award WHERE rule_r3 = 1)::int
    UNION ALL SELECT 'R4 flagged',                         13, (SELECT count(*) FROM fact_award WHERE rule_r4 = 1)::int
    UNION ALL SELECT 'R5 flagged',                       2176, (SELECT count(*) FROM fact_award WHERE rule_r5 = 1)::int
    UNION ALL SELECT 'R6 flagged',                        255, (SELECT count(*) FROM fact_award WHERE rule_r6 = 1)::int
    UNION ALL SELECT 'flagged (score > 0)',             2687, (SELECT count(*) FROM fact_award WHERE risk_score > 0)::int
    UNION ALL SELECT 'band None',                       14179, (SELECT count(*) FROM fact_award WHERE risk_band = 'None')::int
    UNION ALL SELECT 'band Low',                         2490, (SELECT count(*) FROM fact_award WHERE risk_band = 'Low')::int
    UNION ALL SELECT 'band Medium',                       133, (SELECT count(*) FROM fact_award WHERE risk_band = 'Medium')::int
    UNION ALL SELECT 'band High',                          64, (SELECT count(*) FROM fact_award WHERE risk_band = 'High')::int
    UNION ALL SELECT 'score = 9 awards',                   26, (SELECT count(*) FROM fact_award WHERE risk_score = 9)::int
    UNION ALL SELECT 'flagged with no reason',              0, (SELECT count(*) FROM fact_award WHERE risk_score > 0 AND rules_triggered IS NULL)::int
    UNION ALL SELECT 'negative or zero amount',           258, (SELECT count(*) FROM fact_award WHERE award_amount <= 0)::int
)
SELECT check_name, expected, actual,
       CASE WHEN expected = actual THEN 'PASS' ELSE 'FAIL' END AS status
FROM checks
ORDER BY status, check_name;

\echo ''
\echo '================ SECTION 2: amount statistics (compare to the data dictionary) ================'
\echo 'Expected: total ~222.93bn, min ~ -2,024,625, max ~22,428,178,818, avg ~13,200,000, median ~120,031'
SELECT
    round(SUM(award_amount) / 1000000000, 2)                                      AS total_value_bn,
    round(MIN(award_amount), 2)                                                   AS min_amount,
    round(MAX(award_amount), 2)                                                   AS max_amount,
    round(AVG(award_amount), 2)                                                   AS avg_amount,
    round((percentile_cont(0.5) WITHIN GROUP (ORDER BY award_amount))::numeric, 2) AS median_amount
FROM fact_award;

\echo ''
\echo '================ SECTION 3: award value by risk band (expect High ~108, Medium ~64, Low ~33, None ~18) ================'
SELECT risk_band,
       round(SUM(award_amount) / 1000000000, 2) AS value_bn,
       count(*)                                 AS awards
FROM fact_award
GROUP BY risk_band
ORDER BY value_bn DESC;

\echo ''
\echo '================ SECTION 4: full risk score distribution (compare to rule specifications) ================'
SELECT risk_score, count(*) AS awards
FROM fact_award
GROUP BY risk_score
ORDER BY risk_score DESC;

\echo ''
\echo '================ SECTION 5: the Boeing flagship award (expect score 9, band High, R1 R2 R5 R6) ================'
SELECT award_id,
       round(award_amount, 2) AS award_amount,
       rule_r1, rule_r2, rule_r3, rule_r4, rule_r5, rule_r6,
       risk_score, risk_band, rules_triggered
FROM fact_award
WHERE award_id = 'NAS1510000';

\echo ''
\echo '================ verification complete ================'