# Rule Specifications

**Project:** Federal Spending Anomaly Detection
**Author:** Hari Acharya
**Satisfies:** FR-04 (flag suspicious awards by rule) and FR-05 (weighted risk score)
**Implemented in:** sql/03_rules.sql, run against the curated table fact_award (16,866 awards)

## Purpose

This document defines the six anomaly rules and the weighted risk score used to prioritize NASA contract awards for review. For each rule it records the reasoning, the exact threshold, the weight, and how many awards it flagged when the rules were run.

A point on intent. These rules flag awards for a human to review. They do not declare fraud. A flagged award is one that has a shape worth a second look, and many flagged awards will turn out to be perfectly legitimate. That is the correct stance for this kind of screening tool.

## How the rules and the score work

Each rule sets its own flag column on fact_award, with the value 1 if the award is flagged and 0 if not, named rule_r1 through rule_r6. The weighted risk score is the sum of the weights of every rule an award triggers, stored in risk_score. Awards are then ranked by that score so a reviewer can start at the top. Each rule block in the SQL resets its own flag before recomputing, so the whole file is safe to run again.

Two consistent choices across the rules. The dollar based rules (R1, R2, R4) only consider positive amounts, so de-obligations and zero dollar records do not trip them. Awards missing a value needed by a rule, such as the one award with no start date, simply go unflagged by that rule rather than being forced.

## Summary

| Rule | Name | An award is flagged when | Weight | Awards flagged |
|---|---|---|---|---|
| R1 | Large outlier amount | Its amount is above the 99th percentile of all positive amounts, about 207.4 million dollars | 3 | 167 |
| R2 | Vendor spike | Its amount is more than 5 times its recipient's average, for recipients with at least 3 awards | 3 | 291 |
| R3 | Possible threshold splitting | It sits just below a federal limit, 237,500 to 250,000, or 9,500 to 10,000 | 2 | 216 |
| R4 | Round dollar amount | Its amount is an exact multiple of 1,000,000 dollars | 1 | 13 |
| R5 | High vendor concentration | Its recipient's total dollars are in the top 1 percent of all recipients | 2 | 2,176 |
| R6 | Period of performance integrity | The end date is before the start date, or the period is longer than ten years | 1 | 255 |

## Rule detail

### R1 Large outlier amount (weight 3)

An award whose dollar amount is extreme compared to the whole portfolio deserves attention. The threshold is the 99th percentile of all positive award amounts, which came out to about 207.4 million dollars, so R1 flags the top 1 percent of positive awards. It flagged 167 awards. The largest is the Boeing award at 22.4 billion dollars, which is a contract ceiling rather than money spent, and the flagged list reads as the expected roster of major NASA primes.

### R2 Vendor spike (weight 3)

An award far above a recipient's own normal award size can signal an unusual, one off, or mis-keyed award. The threshold is an amount more than five times that recipient's average award amount, restricted to recipients with at least three awards so the average is meaningful, and to positive amounts. It flagged 291 awards. The most extreme run 40 to 90 times a vendor's typical award, for example an Aerospace Corporation award at 93 times their norm. This is the rule taken from the project roadmap.

### R3 Possible threshold splitting (weight 2)

Awards deliberately sized to fall just under a federal competition threshold can indicate splitting work to avoid the oversight that begins above the limit. Using the FY2022-2023 federal limits, the rule flags an amount in the top 5 percent just below either the simplified acquisition threshold of 250,000 dollars (so 237,500 up to 250,000) or the micro purchase threshold of 10,000 dollars (so 9,500 up to 10,000). It flagged 216 awards, 189 just under 250,000 and 27 just under 10,000, with many landing within a few dollars of the limit. Sitting just under the simplified acquisition threshold is often legitimate, so these are review candidates, not findings.

### R4 Round dollar amount (weight 1)

An award for an exact round figure often reflects an estimate or a negotiated lump sum rather than a competed, itemized price. The threshold is a positive amount that is an exact multiple of 1,000,000 dollars. It is weak on its own, which is why it carries weight 1, but it adds signal when it stacks with other rules. It flagged 13 awards, all clean round figures such as 31 million, 5 million, and 2 million.

### R5 High vendor concentration (weight 2)

A small number of recipients receiving an outsized share of total dollars is a known concentration and competition risk. The rule flags every award belonging to a recipient whose total dollars across all their awards are in the top 1 percent of all recipients, the 99th percentile of recipient totals. It flagged 2,176 awards across 41 recipients. The count is larger than the other rules because two of those recipients, Caltech (which runs the Jet Propulsion Laboratory) and Johns Hopkins APL, each hold hundreds of task orders.

### R6 Period of performance integrity (weight 1)

A period that ends before it starts is a data integrity error, and a period running longer than ten years can point to an open ended vehicle worth a closer look. The rule flags an award whose end date is before its start date, or whose period is longer than ten years (more than 3,650 days). It flagged 255 awards, 8 with an end before the start and 247 over ten years. The longest is an AT&T award with a period from 1962 to 2023, about 61 years, a clear example of a long lived vehicle that a reviewer would want to understand.

## Weighted risk score

The risk score is the sum of the weights of the rules an award triggers:

risk_score = 3*R1 + 3*R2 + 2*R3 + 1*R4 + 2*R5 + 1*R6

The maximum possible score is 12. In practice no award scored above 9, because the small dollar rules R3 and R4 almost never occur on the same award as the large outlier and spike rules, which keeps the real ceiling lower than the theoretical one.

## Score distribution

| Risk score | Awards |
|---|---|
| 9 | 26 |
| 8 | 36 |
| 7 | 2 |
| 6 | 48 |
| 5 | 51 |
| 4 | 34 |
| 3 | 315 |
| 2 | 2,091 |
| 1 | 84 |
| 0 | 14,179 |

In total 2,687 awards carry at least one flag and 14,179 are clean, so the model concentrates attention on about 16 percent of the data and clears the rest.

## Top scoring awards

The 26 awards scoring 9 share the same fingerprint, R1, R2, R5, and R6 all firing, meaning large for the portfolio, large for the vendor, from a top concentration vendor, and over a long period. They are the expected major primes: Boeing, Lockheed Martin, Northrop Grumman, Caltech, Raytheon, General Dynamics, and Johns Hopkins APL. The single highest is the Boeing award at 22.4 billion dollars, which is the headline example for the project, one row that touches four rules at once.

## Notes and limitations

- The rules are deliberately simple and rule based. This is appropriate for a first version, and a machine learning approach is noted as a possible future enhancement rather than a requirement.
- Thresholds were set by running each rule and inspecting what it flagged, not guessed in the abstract, so each number is justified by the result it produced.
- A flag means review, not wrongdoing. The legitimate uses of simplified acquisition and of long lived contract vehicles are the clearest examples.
- One award has no start date and so cannot be judged by R6, and 7 awards have no NAICS code, which does not affect these rules but is recorded in the data dictionary.