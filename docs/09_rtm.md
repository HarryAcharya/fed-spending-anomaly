# Requirements Traceability Matrix (RTM)

**Project:** Federal Spending Anomaly Detection
**Author:** Hari Acharya
**Purpose:** Show an unbroken line from each business need to the system behavior that answers it, the user story that frames it, the deliverable that implements it, and the test case that proves it. This is the document a reviewer uses to confirm nothing was promised and left unbuilt, and nothing was built without a reason.

## How to read this matrix

Each row starts at a functional requirement and traces outward: up to its parent business requirement, across to the user story it serves, down to the deliverables that implement it, and finally to the test case that verifies it and its result.

## Traceability matrix

| Business requirement | Functional requirement | User story | Deliverable | Test case | Status |
|---|---|---|---|---|---|
| BR-01 Bring data together | FR-01 Retrieve federal award data | US-01 | python/ingest_awards.py; data/awards_raw.csv | TC-01 | Pass |
| BR-01 Bring data together | FR-02 Store the award data | US-01 | python/db_stage.py; table stg_awards_raw | TC-01 | Pass |
| BR-02 Accurate and consistent data | FR-03 Clean and standardize the data | US-02 | python/build_clean.py; table stg_awards_clean; sql/create_star_schema.sql; sql/load_star_schema.sql; docs/05_data_dictionary.md | TC-02 | Pass |
| BR-03 Identify unusual awards | FR-04 Flag awards that look unusual | US-03 | sql/03_rules.sql (rules R1 to R6); docs/06_rule_specifications.md; sql/test_r3_threshold_split.sql | TC-03 | Pass |
| BR-04 Show how risky each award is | FR-05 Score and rank awards by risk | US-04 | sql/03_rules.sql (risk_score); fact_award.risk_score | TC-04 | Pass |
| BR-05 Explain why each award was flagged | FR-06 Show the reason behind each flag | US-05, US-07 | sql/03_rules.sql (rules_triggered); Anomaly Review table in Power BI and Tableau | TC-05 | Pass |
| BR-06 Accessible presentation | FR-07 Present results in accessible dashboards | US-06, US-07, US-08 | Power BI dashboard; Tableau Public dashboard; docs/07_accessibility_review.md | TC-06 | Pass with notes |

## Coverage summary

- All six business requirements (BR-01 to BR-06) trace to at least one functional requirement.
- All seven functional requirements (FR-01 to FR-07) trace to a user story, a deliverable, and a test case.
- All eight user stories (US-01 to US-08) are represented: US-01 in FR-01 and FR-02, US-02 in FR-03, US-03 in FR-04, US-04 in FR-05, US-05 in FR-06, US-06 in FR-07, US-07 in FR-06 and FR-07, US-08 in FR-07.
- All six test cases (TC-01 to TC-06) pass. TC-06 passes with documented notes, recorded in the test cases document, covering the single agency substitutions and two recommended accessibility refinements.

The chain is unbroken from business need to proven result. Nothing in the build lacks a business reason, and nothing the business asked for is missing a test that checks it.