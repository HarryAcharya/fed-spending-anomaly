# Test Cases and Results

**Project:** Federal Spending Anomaly Detection
**Author:** Hari Acharya
**Purpose:** Prove that each functional requirement was met. Every test case is tied to the functional requirements and user stories it checks, and records the steps, the expected result, the actual result, and a pass or fail status.

## Summary

| Test case | Title | Covers | Status |
|---|---|---|---|
| TC-01 | Data retrieval and storage | FR-01, FR-02, US-01 | Pass |
| TC-02 | Data cleaning and standardization | FR-03, US-02 | Pass |
| TC-03 | Rule flagging | FR-04, US-03 | Pass |
| TC-04 | Risk score and ranking | FR-05, US-04 | Pass |
| TC-05 | Reason shown for each flag | FR-06, US-05, US-07 | Pass |
| TC-06 | Accessible dashboards and cross tool match | FR-07, US-06, US-07, US-08 | Pass with notes |

## TC-01: Data retrieval and storage

Covers FR-01, FR-02 and US-01.

Steps:
1. Run ingest_awards.py to pull NASA prime contract awards (types A, B, C, D) active during FY2022 and FY2023 from the USASpending API, with retries on network errors.
2. Run db_stage.py to load the raw CSV into the staging table stg_awards_raw.
3. Count the rows.

Expected: all in scope records are retrieved and stored exactly as received before any cleaning, and the record count is reported.

Actual: 16,866 unique awards were pulled, deduplicated by the permanent identifier generated_internal_id, and loaded into stg_awards_raw, with 16,866 rows confirmed.

Status: Pass.

## TC-02: Data cleaning and standardization

Covers FR-03 and US-02.

Steps:
1. Run build_clean.py to produce the curated table stg_awards_clean.
2. Check the row count, the distinct counts, and any values that could not be parsed.

Expected: recipient names are standardized, exact duplicates are removed, codes and dates are parsed, each award links to a recipient, a date, and an industry code, and a cleaning note is recorded.

Actual: stg_awards_clean has 16,866 rows, 4,064 recipients, 412 NAICS codes, 779 PSC codes, 0 unparsed amounts, 1 unparsed start date, and 0 unparsed end dates. The cleaning is documented in the data dictionary.

Status: Pass.

## TC-03: Rule flagging

Covers FR-04 and US-03.

Steps:
1. Run sql/03_rules.sql to apply the six rules.
2. Count the awards flagged by each rule.
3. Run the seeded known case sql/test_r3_threshold_split.sql.

Expected: each of the six rules flags the awards matching its pattern, an award can be flagged by more than one rule, and a synthetic award sized at 249,999 trips only R3.

Actual: R1 flagged 167, R2 flagged 291, R3 flagged 216, R4 flagged 13, R5 flagged 2,176, R6 flagged 255. Awards that trip several rules exist, for example the top awards trip R1, R2, R5, and R6 together. The seeded 249,999 award returned rule_r3 = 1 and every other rule 0, with a score of 2, then rolled back so the real data was untouched.

Status: Pass.

## TC-04: Risk score and ranking

Covers FR-05 and US-04.

Steps:
1. Compute risk_score in sql/03_rules.sql as the weighted sum of triggered rules (R1 weight 3, R2 weight 3, R3 weight 2, R4 weight 1, R5 weight 2, R6 weight 1).
2. Inspect the score distribution.
3. Verify the score on a known award.
4. Sort by score.

Expected: every award carries a score equal to the weighted sum of the rules it triggered, the maximum possible is 12, and awards can be ranked highest to lowest.

Actual: scores range from 0 to 9, from 14,179 awards at 0 up to 26 awards at 9. The Boeing award NAS1510000 triggers R1, R2, R5, and R6, which is 3 + 3 + 2 + 1 = 9, and it shows a risk_score of 9. Awards sort correctly from highest to lowest in both dashboards.

Status: Pass.

## TC-05: Reason shown for each flag

Covers FR-06, US-05 and US-07.

Steps:
1. Check the rules_triggered value for flagged awards.
2. Confirm no flagged award has a blank reason.
3. Confirm the dashboards display the reason.

Expected: every flagged award lists the rules that triggered it in plain terms, and no award is ever shown as flagged without a reason.

Actual: rules_triggered is populated for all 2,687 flagged awards, for example R1, R2, R5, R6, and it appears in the Anomaly Review table in both dashboards. Because the same rule flags drive both the score and the label, any award with a score above zero always has at least one reason, so no flagged award is blank.

Status: Pass.

## TC-06: Accessible dashboards and cross tool match

Covers FR-07, US-06, US-07 and US-08.

Steps:
1. Build the Power BI dashboard and the Tableau dashboard from the curated data.
2. Compare the headline numbers across the two tools.
3. Review the dashboards against WCAG 2.1 AA.

Expected: both tools show a leadership summary and a ranked review view, the headline numbers match, and meaning is never carried by color alone.

Actual: both dashboards show the four headline numbers ($222.93bn total award value, 16,866 awards, 2,687 flagged, 64 high risk), the risk band and recipient charts, and the ranked Anomaly Review table, and the headline numbers match across Power BI and Tableau. Risk level and the triggered rules are shown as text, so color is never the only signal.

Status: Pass with notes.

Notes, recorded honestly:
- US-06 lists spending by agency. Because the dataset is a single agency (NASA), an agency breakdown adds nothing, so it was substituted with spending by risk band and by top recipient. This matches the deliberate decision not to build an agency dimension.
- US-06 also lists a spending trend over time. Because award dates span many years and join on the period end, a raw time trend was misleading on a one screen overview, so it was substituted with the Award Value by Risk Band view. A start date trend is noted as a possible future addition.
- US-07 drill into a single award is met through the Anomaly Review table, which shows each award's recipient, amount, risk score, and triggered rules. A dedicated single award drill through page is a possible enhancement.
- US-08 keyboard navigation and a text description for every visual are partially met. The accessibility review records these as recommended refinements for a production version.

## Conclusion

All six test cases pass. TC-06 passes with documented notes where the single agency dataset and the date structure led to honest substitutions, and where two accessibility refinements are recommended for production. Every functional requirement, FR-01 through FR-07, is proven by at least one test case.