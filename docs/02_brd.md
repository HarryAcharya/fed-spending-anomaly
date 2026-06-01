# Business Requirements Document (BRD)
## Federal Spending Anomaly Detection

Prepared by: Hari Acharya
Date: May 31, 2026
Version: 1.0
Status: Approved baseline

## Purpose of this document

This document lists what the business needs from the solution and why. It is written in plain business language and does not describe how the solution will be built. The how is covered in the Functional Requirements Document that comes next.

Each requirement has an ID from BR-01 to BR-06. These IDs are used through the rest of the project so that every requirement can be traced from the business need all the way to the test that proves it was met.

## How to read this document

Each requirement has a short statement of the need, a note on why it matters to the business, and a priority. The priority uses a simple scale:

- Must have. The project fails its purpose without this.
- Should have. Important and expected, but the core value still holds if it is reduced.
- Could have. A nice addition if time allows.

## Business requirements

### BR-01: Bring award spending data together in one place

The business needs all the federal award records it wants to review collected into one consistent, reliable source. Today the information sits in a public system that is not built for the kind of review work the team needs to do.

Why this matters: reviewers cannot look for unusual patterns if the data is scattered or hard to reach. A single trusted source is the foundation for everything else.

Priority: Must have

### BR-02: Make sure the data is accurate and consistent

The business needs the award data to be clean and consistent before anyone draws conclusions from it. Names, amounts, and dates should mean the same thing every time they appear.

Why this matters: if the same vendor shows up under three slightly different names, the review will miss patterns and reviewers will lose trust in the results. Decisions based on messy data cannot be defended.

Priority: Must have

### BR-03: Identify awards that look unusual

The business needs a way to automatically point out awards that do not fit normal spending patterns, so they can be looked at more closely. Examples of unusual patterns include a payment far larger than a vendor normally receives, or several awards that sit just below a dollar limit that would have required extra approval.

Why this matters: there are far too many awards to review by hand. The team needs the unusual ones surfaced for them rather than searching blindly.

Priority: Must have

### BR-04: Show how risky each flagged award is

The business needs each flagged award to carry a clear measure of how concerning it is, so reviewers can start with the awards that matter most.

Why this matters: a long flat list of flags is not much better than no list at all. Reviewers have limited time and need to know what to look at first.

Priority: Must have

### BR-05: Explain why each award was flagged

The business needs reviewers to be able to see, in plain terms, the reason an award was flagged. A reviewer should never face a flag with no explanation behind it.

Why this matters: reviewers have to act on these flags and often have to justify their decisions to others. A flag they cannot explain is a flag they cannot use or defend.

Priority: Should have

### BR-06: Present the results so anyone can use them, including people with disabilities

The business needs the results shown in a clear, visual summary that non technical staff can understand at a glance. The summary must also meet federal accessibility requirements so that people with disabilities can use it equally.

Why this matters: the people reviewing these awards are not analysts and will not read raw data. As a federal solution it also has to be accessible to everyone by law, not as an afterthought.

Priority: Must have

## Baseline note

These six requirements form the agreed baseline for the project. Any change to them is recorded by raising the version number of this document, so the history stays clear.
