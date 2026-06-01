# User Stories and Acceptance Criteria
## Federal Spending Anomaly Detection

Prepared by: Hari Acharya
Date: May 31, 2026
Version: 1.0
Status: Approved baseline

## Purpose of this document

This document describes the solution from the point of view of the people who will use it. Each story says who the person is, what they want, and why they want it. Each one also lists acceptance criteria, which are the conditions that must be true for the story to count as done.

The stories use the standard Agile format:

As a [type of user], I want [a goal], so that [a reason].

Each story has an ID from US-01 to US-08 and is tagged with the functional and business requirements it relates to. This keeps the line from the user need through to the requirements and, later, to the test cases.

## The users

- Reviewer. A compliance or oversight analyst who reviews flagged awards. This is the main user.
- Director. The business lead who owns the review process.
- CFO. The executive sponsor who wants the high level picture.
- Data Analyst. The person who builds and maintains the data behind the solution.

## User stories

### US-01: Collect the award data in one place
As a Data Analyst, I want all the award records pulled into one place, so that I have a complete and reliable dataset to work from.

Related requirements: FR-01, FR-02 (BR-01)

Acceptance criteria:
- Award records for the agencies and fiscal years in scope are retrieved from the USASpending API.
- The number of records retrieved is reported, so the volume is known.
- All records are stored as received before any cleaning takes place.
- If the source returns an error, the system retries rather than stopping silently.

### US-02: Trust that the data is clean
As a Reviewer, I want the data to be clean and consistent, so that I can trust the patterns I see and the same vendor is not split across different spellings.

Related requirements: FR-03 (BR-02)

Acceptance criteria:
- Recipient names are trimmed and put into a consistent format.
- Exact duplicate records are removed.
- Each award links to a single agency, recipient, date, and industry code.
- A short note records what cleaning was applied and how many rows it affected.

### US-03: Have unusual awards flagged for me
As a Reviewer, I want awards that look unusual to be flagged automatically, so that I do not have to read every award by hand.

Related requirements: FR-04 (BR-03)

Acceptance criteria:
- Each of the six rules flags the awards that match its pattern.
- An award can be flagged by more than one rule at the same time.
- Every rule has a written reason and a defined threshold on record.

### US-04: See the riskiest awards first
As a Reviewer, I want flagged awards ranked by a risk score, so that I can start with the ones that matter most.

Related requirements: FR-05 (BR-04)

Acceptance criteria:
- Every award has a risk score.
- The score reflects the weights of the rules the award triggered.
- Awards can be sorted from the highest score to the lowest.

### US-05: Understand why an award was flagged
As a Reviewer, I want to see why each award was flagged, so that I can act on it and explain my decision to others.

Related requirements: FR-06 (BR-05)

Acceptance criteria:
- For any flagged award, the rules that triggered it are listed in plain language.
- No award is ever shown as flagged without at least one reason attached.

### US-06: Get a quick high level picture
As the CFO, I want a high level summary of total spending and how many awards were flagged, so that I can understand the picture at a glance without reading raw data.

Related requirements: FR-07 (BR-06)

Acceptance criteria:
- The summary shows total spending, a spending trend over time, spending by agency, and the count of flagged awards.
- The headline numbers match between the Power BI and Tableau versions.

### US-07: Drill into a single award
As a Reviewer, I want to open a single flagged award and see its full detail, so that I can complete my review in one place.

Related requirements: FR-06, FR-07 (BR-05, BR-06)

Acceptance criteria:
- A reviewer can select one award and see its detail view.
- The detail view shows the recipient, agency, amount, risk score, and the rules that were triggered.

### US-08: Use the dashboard with assistive technology
As a Reviewer who uses assistive technology, I want the dashboard to be accessible, so that I can do my job on equal terms with everyone else.

Related requirements: FR-07 (BR-06)

Acceptance criteria:
- Color contrast meets WCAG AA.
- Meaning is never carried by color alone. Labels or icons are used as well.
- The dashboard can be navigated by keyboard in a sensible order.
- Every visual has a title and a text description.

## Coverage check

Every functional requirement is reflected in at least one user story:

- FR-01 and FR-02 appear in US-01
- FR-03 appears in US-02
- FR-04 appears in US-03
- FR-05 appears in US-04
- FR-06 appears in US-05 and US-07
- FR-07 appears in US-06, US-07, and US-08

This keeps the chain unbroken from business need, to system behavior, to the people who use it.
