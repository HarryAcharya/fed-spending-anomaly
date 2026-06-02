-- test_r3_threshold_split.sql
-- Federal Spending Anomaly Detection
-- Phase 4, Step 19: a known test case for the rule engine.
--
-- We insert one synthetic award built to trip rule R3 (threshold
-- splitting) and nothing else: amount 249,999, a brand new vendor
-- with no other awards, and no dates. We then re-run the real rule
-- engine on it and show the result. Expected: rule_r3 = 1, every
-- other rule = 0, risk_score = 2.
--
-- The whole thing runs inside a transaction that is rolled back at
-- the end, so the real data stays untouched at 16,866 awards.

BEGIN;

-- a dedicated test vendor so R2 and R5 cannot be affected
INSERT INTO dim_recipient (recipient_name)
VALUES ('TEST VENDOR THRESHOLD SPLIT');

-- the synthetic award, sized one dollar under the 250,000 limit
INSERT INTO fact_award (generated_internal_id, award_id, recipient_key, award_amount)
SELECT 'TEST_R3_0001', 'TEST-R3-0001', recipient_key, 249999.00
FROM dim_recipient
WHERE recipient_name = 'TEST VENDOR THRESHOLD SPLIT';

-- re-run the actual rule engine over the whole table, test row included
\i sql/03_rules.sql

-- show how the engine scored the test award
SELECT generated_internal_id, award_amount,
       rule_r1, rule_r2, rule_r3, rule_r4, rule_r5, rule_r6, risk_score
FROM fact_award
WHERE generated_internal_id = 'TEST_R3_0001';

-- undo everything, leaving the real data exactly as it was
ROLLBACK;