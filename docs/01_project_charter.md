# Project Charter
## Federal Spending Anomaly Detection

Prepared by: Hari Acharya
Date: May 31, 2026
Version: 1.0
Status: Approved baseline for the project

## Purpose of this document

This charter explains why the project exists, what it will deliver, who it is for, and how we will know it worked. It is the first document in the project and everything else builds on it. If someone new picks up this repository, this page should tell them what they are looking at in a few minutes.

## A note on the setup

This is a portfolio project built by one person to show end to end analytics skill. The data is real and public, pulled from the USASpending API, but the stakeholders and the review team described below are simulated. I am playing the role of the business analyst and data analyst on the engagement. I treat the work as if it were a real assignment so the documents and decisions reflect how this would run inside an actual federal office.

## Business problem

Every year the federal government awards a very large amount of money through contracts. Most of that spending is normal and follows the rules. A small share of it carries errors, waste, or early signs of fraud, such as a payment that is far larger than a vendor usually receives, or several awards that sit just under a dollar limit that would have required extra approval.

The problem is volume. Oversight and compliance reviewers cannot read every award by hand. There are far too many. Without a way to narrow the list, they either spend time on awards that turn out to be fine, or they miss the ones that needed a closer look. They need help deciding where to focus.

## Project objective

Build a working analytics solution that pulls real federal award data, flags awards that look unusual using a clear and documented set of rules, scores each award by how risky it appears, and presents the results in dashboards that a non technical reviewer can actually use. The goal is simple. Help reviewers spend their limited time on the awards most worth a second look, and be able to explain why each award was flagged.

## Scope

In scope for this project:

- Public award data from the USASpending API, focused on prime contract awards.
- A small number of federal agencies and a defined fiscal year window. The exact agency or agencies and the years are confirmed in Phase 2 once I see how much data each one returns. The target is a meaningful slice in the range of tens of thousands of records.
- A PostgreSQL database with a raw staging layer and a clean curated star schema.
- Six rule based anomaly detectors and a weighted risk score that ranks awards for review.
- Two dashboards that show the same results, one in Power BI and one in Tableau.
- A Section 508 accessibility review of the dashboards.
- A full set of business analysis documents that trace from business need to test result.

Out of scope for this project:

- Real time or streaming data. The data is pulled in batches and refreshed by hand.
- Machine learning models. The first version uses clear rules that anyone can read and check. Machine learning is noted as a possible future enhancement, not part of this build.
- Any private or personally identifiable information. Only public data is used.
- Making the final call on an award. The tool helps a reviewer decide where to look. A human still makes the decision.

## Stakeholders

The roles below are simulated for this portfolio project. They describe who the solution is built for and what each person cares about.

| Role | Title | What they care about |
| --- | --- | --- |
| Project Sponsor | Chief Financial Officer | Protecting funds and reducing waste and improper payments |
| Business Lead | Director, Office of Financial Oversight | A review process that is faster and easier to defend |
| End Users | Compliance and oversight analysts | A short, ranked list of awards to review and a clear reason for each flag |
| Data Source Owner | USASpending program | Correct and responsible use of public award data |
| Analyst and Builder | MSDA student (me) | Delivering the full solution and the documentation behind it |

## Success criteria

The project is a success when all of the following are true:

- The pipeline pulls a meaningful slice of award data from the API into the database, on the order of tens of thousands of records.
- All six detection rules are built and documented, and every award in the curated layer carries a risk score.
- When I sort awards by risk score, the awards at the top make sense as things a reviewer would want to check.
- The Power BI and Tableau dashboards show the same headline numbers and both allow a reviewer to drill into a single flagged award.
- The dashboards pass a basic Section 508 review, including color contrast at WCAG AA and not relying on color alone.
- The full document set is complete and the Requirements Traceability Matrix links every business requirement to a functional requirement, a user story, a deliverable, and a test case with no gaps.
- A person who has never seen the project can clone the repository and reproduce the results using the README alone.

## Assumptions and constraints

- The work is done by one person (Hari Acharya) on a personal Windows laptop, using only free and public tools and data.
- There is no budget and no production environment. Everything runs locally.
- The data is historical and is refreshed manually, not on a schedule.
- The stakeholders and review team are simulated, as noted above.

## High level deliverables

The project produces a GitHub repository containing the data pipeline, the SQL models, the rule engine, both dashboards, and the full document set, plus a short portfolio write up and a recorded walkthrough at the end. The complete list is tracked in the Master Deliverables Checklist in the roadmap.
