# Functional Requirements Document (FRD)
## Federal Spending Anomaly Detection

Prepared by: Hari Acharya
Date: May 31, 2026
Version: 1.0
Status: Approved baseline

## Purpose of this document

This document describes what the system will do to meet each business need listed in the BRD. Where the BRD said what the business needs and why, this document says how the system answers it.

Each functional requirement has an ID from FR-01 to FR-07 and is tagged with the parent business requirement it comes from. This keeps a clear line from the business need to the system behavior, which we complete later in the Requirements Traceability Matrix.

## How to read this document

Functional requirements are written using the phrase "The system shall." Each one has the requirement, the parent business requirement it satisfies, and a short note that explains what it covers in practice.

## Functional requirements

### FR-01: Retrieve federal award data
The system shall retrieve federal prime contract award records from the USASpending public API for the agencies and fiscal years that are in scope.

Parent requirement: BR-01

Note: The system pulls the fields needed for review, such as the award identifier, recipient, amount, awarding agency, dates, location, and industry code. It keeps retrieving until all matching records for the chosen scope have been collected.

### FR-02: Store the award data
The system shall store the retrieved records in a database so they can be queried and analyzed in a consistent way.

Parent requirement: BR-01

Note: The records are first kept exactly as received in a separate staging area, before any changes are made, so the original data is always available to go back to.

### FR-03: Clean and standardize the data
The system shall clean and standardize the stored data into a consistent model that is ready for analysis.

Parent requirement: BR-02

Note: This includes trimming and standardizing recipient names, fixing inconsistent capitalization, removing exact duplicates, and organizing the data so each award links cleanly to its agency, recipient, date, and industry code.

### FR-04: Flag awards that look unusual
The system shall apply a set of documented rules that flag awards matching defined unusual patterns.

Parent requirement: BR-03

Note: Each rule checks for one specific pattern, such as an amount far above a recipient's normal level. Six rules are planned, named R1 through R6, and each one has a written reason and a defined threshold.

### FR-05: Score and rank awards by risk
The system shall give each award a weighted risk score based on the rules it triggered, and allow awards to be ranked from most to least concerning.

Parent requirement: BR-04

Note: Each rule carries a weight. An award's score is the total of the weights of the rules it triggered, so awards that trip several rules or more serious rules rise to the top of the list.

### FR-06: Show the reason behind each flag
The system shall record and display which rules each flagged award triggered, so a reviewer can see the reason behind every flag.

Parent requirement: BR-05

Note: When a reviewer opens an award, the rules it triggered are listed in plain terms next to its risk score, so no flag is ever shown without an explanation.

### FR-07: Present results in accessible dashboards
The system shall present the results in visual dashboards that meet federal Section 508 accessibility standards.

Parent requirement: BR-06

Note: This includes meeting WCAG AA color contrast and never relying on color alone to carry meaning. The dashboards provide a high level summary for leadership and a ranked review view for analysts, with the ability to drill into a single award.

## Coverage check

Every business requirement is covered by at least one functional requirement:

- BR-01 is met by FR-01 and FR-02
- BR-02 is met by FR-03
- BR-03 is met by FR-04
- BR-04 is met by FR-05
- BR-05 is met by FR-06
- BR-06 is met by FR-07

No business requirement is left without a matching system behavior, and no functional requirement exists without a business reason behind it.
