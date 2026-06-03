# Federal Spending Anomaly Detection

An end to end analytics project that pulls real federal contract award data, models it in a database, applies rule based anomaly detection with a weighted risk score, and presents the results in accessible Power BI and Tableau dashboards. Every step traces from a business need to the test that proves it.

**A note on honesty:** the data is real and public, pulled from the USASpending API. The stakeholders and review team are simulated for this portfolio project. The dataset is NASA prime contract awards (types A, B, C, D) that were active during fiscal years 2022 and 2023, October 2021 through September 2023.

## Live dashboard

Tableau Public: https://public.tableau.com/app/profile/hari.acharya2369/viz/NASAFederalSpendingAnomalyDetection/AnomalyOverview

## What it does

The project takes 16,866 NASA contract awards from a public API, cleans and models them into a star schema, runs six documented rules that flag awards with unusual patterns, gives each award a weighted risk score so reviewers can start with the most concerning ones, and shows the whole picture in two dashboards built in different tools that agree to the dollar.

## The business problem

Federal award data sits in a public system that is not built for review work. There are far too many awards to read by hand, so the team needs the unusual ones surfaced and ranked, with a plain reason attached to each flag, presented so that non technical and assistive technology users can both use it.

## Architecture

The data moves through clearly separated stages, so ingestion, cleaning, and modeling never blur together.

A visual version of the pipeline is in docs/process_flow.png.

## Key results

- 16,866 unique awards, 4,064 recipients, 412 NAICS codes, 779 PSC codes.
- Six anomaly rules R1 to R6, each with a written reason and a defined threshold, combined into a weighted risk score from 0 to a maximum of 12.
- 2,687 awards carry at least one flag (about 16 percent), 64 are High risk, and 14,179 are clean.
- The single highest risk award is a Boeing contract with a 22.4 billion dollar ceiling that trips four rules at once (large outlier, vendor spike, vendor concentration, and a long period of performance) for a score of 9.
- The Power BI and Tableau dashboards show identical headline numbers, which is the cross tool check that the results are sound.

## Tech stack

Python 3.14, PostgreSQL 17, Power BI, Tableau Public, Git and GitHub.

## Repository structure

## Documentation

The full business analysis artifact set, traceable end to end:

- docs/01_project_charter.md
- docs/02_brd.md, six business requirements
- docs/03_frd.md, seven functional requirements
- docs/04_user_stories.md, eight user stories
- docs/05_data_dictionary.md
- docs/06_rule_specifications.md, the six rules with thresholds and results
- docs/07_accessibility_review.md, the Section 508 review
- docs/08_test_cases.md, six test cases and results
- docs/09_rtm.md, the requirements traceability matrix

## How to reproduce

1. Create and activate a virtual environment, then `pip install -r requirements.txt`.
2. Create a PostgreSQL database named fed_spending and put the password in a .env file in the project root.
3. `python python/ingest_awards.py` to pull the awards into data/awards_raw.csv.
4. `python python/db_stage.py` to load the staging table.
5. `python python/build_clean.py` to build the clean table.
6. `psql -U postgres -d fed_spending -f sql/create_star_schema.sql` to create the star schema.
7. `psql -U postgres -d fed_spending -f sql/load_star_schema.sql` to load it.
8. `psql -U postgres -d fed_spending -f sql/03_rules.sql` to run the rules and score.
9. Optional: `psql -U postgres -d fed_spending -f sql/test_r3_threshold_split.sql` to run the seeded test case.
10. Open the Power BI file in dashboards, or connect Tableau to the exported CSV, to view the dashboards.

## Accessibility

The dashboards were reviewed against Section 508 and WCAG 2.1 AA. Risk level and the triggered rules are always shown as text, so meaning is never carried by color alone. The full review and its recommendations are in docs/07_accessibility_review.md.

## Honest notes and limitations

- The dataset is a single agency, NASA, so there is no agency dimension and no agency breakdown. This was a deliberate modeling choice.
- The award amount is the obligated and ceiling value, not money actually spent, so the largest figures are contract ceilings rather than cash out the door.
- The dataset is awards active during the window, not awards that started in it, because the API matches awards with activity in the window.
- The rules deliberately target large and concentrated awards, so the flagged set naturally holds most of the dollar value. The dashboards focus a reviewer on that small set rather than claiming it is fraud.
- The stakeholders and review team are simulated. The data and the analysis are real.

## Author

Hari Acharya, MSDA. Built as a portfolio project to demonstrate an analytics effort run end to end, from business requirements through data engineering, rule design, dashboards, accessibility, and full requirements traceability.