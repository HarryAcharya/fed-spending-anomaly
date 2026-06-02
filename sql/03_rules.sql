-- ===========================================================
-- 03_rules.sql
-- Federal Spending Anomaly Detection
-- Phase 4: anomaly detection rules and weighted risk score
-- Author: Hari Acharya
--
-- Each rule sets its own flag column on fact_award (1 if flagged,
-- 0 if not). After all six rules are in place, a final scoring
-- step sums the weights of the triggered rules into risk_score.
-- Every block below is safe to run again.
-- ===========================================================

-- -----------------------------------------------------------
-- R1: Large outlier amount                        Weight 3   FR-04
-- Rationale: an award whose dollar amount is extreme compared to
--   the rest of the portfolio is worth a reviewer's attention.
-- Threshold (v1): award_amount is in the top 1 percent of all
--   positive award amounts, that is, above the 99th percentile.
-- Only positive amounts are considered, so de-obligations and
--   zero dollar records do not trip the rule.
-- -----------------------------------------------------------
ALTER TABLE fact_award ADD COLUMN IF NOT EXISTS rule_r1 smallint DEFAULT 0;
UPDATE fact_award SET rule_r1 = 0;

WITH cutoff AS (
    SELECT percentile_cont(0.99) WITHIN GROUP (ORDER BY award_amount) AS p99
    FROM fact_award
    WHERE award_amount > 0
)
UPDATE fact_award f
SET rule_r1 = 1
FROM cutoff c
WHERE f.award_amount > 0
  AND f.award_amount > c.p99;



  -- -----------------------------------------------------------
-- R2: Vendor spike                                Weight 3   FR-04
-- Rationale: an award far above a recipient's own normal award
--   size can signal an unusual, one off, or mis-keyed award.
-- Threshold: award_amount is more than 5 times that recipient's
--   average award amount. Only recipients with at least 3 awards
--   are considered, so the average is meaningful, and only
--   positive amounts are used. This is the roadmap example rule.
-- -----------------------------------------------------------
ALTER TABLE fact_award ADD COLUMN IF NOT EXISTS rule_r2 smallint DEFAULT 0;
UPDATE fact_award SET rule_r2 = 0;

WITH recipient_avg AS (
    SELECT recipient_key,
           AVG(award_amount) AS avg_amt,
           COUNT(*)          AS n_awards
    FROM fact_award
    WHERE award_amount > 0 AND recipient_key IS NOT NULL
    GROUP BY recipient_key
)
UPDATE fact_award f
SET rule_r2 = 1
FROM recipient_avg a
WHERE f.recipient_key = a.recipient_key
  AND a.n_awards >= 3
  AND f.award_amount > 0
  AND f.award_amount > a.avg_amt * 5;


  -- -----------------------------------------------------------
-- R3: Possible threshold splitting                Weight 2   FR-04
-- Rationale: awards deliberately sized to fall just under a
--   federal competition threshold can be a sign of splitting work
--   to avoid the oversight that kicks in above the limit.
-- Thresholds used (FY2022-2023 federal limits):
--   micro purchase threshold      = 10,000
--   simplified acquisition limit  = 250,000
-- Flagged band: an amount in the top 5 percent just below either
--   limit, that is 9,500 up to 10,000, or 237,500 up to 250,000.
-- -----------------------------------------------------------
ALTER TABLE fact_award ADD COLUMN IF NOT EXISTS rule_r3 smallint DEFAULT 0;
UPDATE fact_award SET rule_r3 = 0;

UPDATE fact_award
SET rule_r3 = 1
WHERE (award_amount >= 9500   AND award_amount < 10000)
   OR (award_amount >= 237500 AND award_amount < 250000);

   -- -----------------------------------------------------------
-- R4: Round dollar amount                          Weight 1   FR-04
-- Rationale: an award for an exact round figure often reflects an
--   estimate or a negotiated lump sum rather than a competed,
--   itemized price. On its own it is weak, hence weight 1, but it
--   adds useful signal when stacked with other rules.
-- Threshold: a positive amount that is an exact multiple of
--   1,000,000 dollars, for example 5,000,000.00.
-- -----------------------------------------------------------
ALTER TABLE fact_award ADD COLUMN IF NOT EXISTS rule_r4 smallint DEFAULT 0;
UPDATE fact_award SET rule_r4 = 0;

UPDATE fact_award
SET rule_r4 = 1
WHERE award_amount > 0
  AND award_amount % 1000000 = 0;

  -- -----------------------------------------------------------
-- R5: High vendor concentration                   Weight 2   FR-04
-- Rationale: a small number of recipients receiving an outsized
--   share of total dollars is a known concentration and
--   competition risk. Awards going to those top recipients are
--   worth keeping in view.
-- Threshold: the recipient's total dollars across all their
--   awards is in the top 1 percent of all recipients, that is at
--   or above the 99th percentile of recipient totals. Every award
--   belonging to such a recipient is flagged.
-- -----------------------------------------------------------
ALTER TABLE fact_award ADD COLUMN IF NOT EXISTS rule_r5 smallint DEFAULT 0;
UPDATE fact_award SET rule_r5 = 0;

WITH recipient_total AS (
    SELECT recipient_key, SUM(award_amount) AS total_amt
    FROM fact_award
    WHERE recipient_key IS NOT NULL
    GROUP BY recipient_key
),
cutoff AS (
    SELECT percentile_cont(0.99) WITHIN GROUP (ORDER BY total_amt) AS p99
    FROM recipient_total
)
UPDATE fact_award f
SET rule_r5 = 1
FROM recipient_total rt, cutoff c
WHERE f.recipient_key = rt.recipient_key
  AND rt.total_amt >= c.p99;


-- -----------------------------------------------------------
-- R6: Period of performance integrity              Weight 1   FR-04
-- Rationale: a period that ends before it starts is a data
--   integrity error, and a period running longer than ten years
--   can point to an open ended vehicle worth a closer look. Weak
--   on its own, hence weight 1.
-- Threshold: end date earlier than start date, OR a period longer
--   than ten years (more than 3,650 days). Awards missing a date
--   cannot be judged and are left unflagged.
-- -----------------------------------------------------------
ALTER TABLE fact_award ADD COLUMN IF NOT EXISTS rule_r6 smallint DEFAULT 0;
UPDATE fact_award SET rule_r6 = 0;

UPDATE fact_award f
SET rule_r6 = 1
FROM dim_date sd, dim_date ed
WHERE f.start_date_key = sd.date_key
  AND f.end_date_key   = ed.date_key
  AND (
        ed.full_date < sd.full_date
     OR ed.full_date - sd.full_date > 3650
      );



-- ===========================================================
-- Weighted risk score                              FR-05
-- The risk score is the sum of the weights of every rule an
-- award triggers, so awards can be ranked for review.
--   R1 large outlier      weight 3
--   R2 vendor spike       weight 3
--   R3 threshold split    weight 2
--   R4 round dollar       weight 1
--   R5 concentration      weight 2
--   R6 PoP integrity      weight 1
-- Maximum possible score is 12.
-- ===========================================================
UPDATE fact_award
SET risk_score =
      3 * rule_r1
    + 3 * rule_r2
    + 2 * rule_r3
    + 1 * rule_r4
    + 2 * rule_r5
    + 1 * rule_r6;