# Executive Summary

**Project:** Federal Spending Anomaly Detection
**Author:** Hari Acharya

## The challenge

Federal agencies award thousands of contracts a year. The records are public, but they sit in a system built for lookup, not for review. With so many awards, no team can read each one, so unusual spending can pass unnoticed. The need is simple to state: surface the awards that look unusual, rank them so reviewers start with the ones that matter most, and explain in plain terms why each was flagged, all in a view that anyone can use.

## What was built

A complete pipeline that takes real, public NASA contract award data and turns it into a prioritized review list. The data is pulled from the USASpending API, cleaned and organized into a database, checked against six documented rules that each look for one unusual pattern, and scored so that the most concerning awards rise to the top. The results are shown in two dashboards, one in Power BI and one in Tableau, that any reviewer or executive can read at a glance.

## What we found

Across 16,866 NASA contract awards active in fiscal years 2022 and 2023:

- 2,687 awards, about 16 percent, were flagged by at least one rule. The other 84 percent were clean and can be set aside.
- Only 64 awards landed in the highest risk band, yet those 64 awards account for roughly 108 billion dollars of award value. A very small number of awards holds a large share of the money, which is exactly where review attention belongs.
- The single highest risk award is a Boeing contract with a 22.4 billion dollar ceiling that trips four rules at once. It is a real, explainable award, but precisely the kind a reviewer should see first.

## Why it matters

The tool turns an unreadable pile of awards into a short, ranked list with a reason attached to every flag. A reviewer can open the top of the list, see that an award is large for its vendor, concentrated, and long running, and decide what to do, then justify that decision to others. It does not accuse anyone of wrongdoing. It focuses limited review time on the awards most worth a closer look. The dashboards meet federal accessibility standards, so staff who rely on assistive technology can use them on equal terms.

## Honest scope

The data and the analysis are real. The stakeholders and review team are simulated for this portfolio project. The award amounts are obligated and ceiling values, so the largest figures are contract ceilings rather than money already spent, and the dataset covers a single agency, NASA. These choices are documented openly throughout the project so the numbers are never read as more than they are.

## In one line

A small, well chosen set of rules turns 16,866 federal awards into a ranked, explained, accessible review list that points a reviewer straight at the awards that hold most of the risk.