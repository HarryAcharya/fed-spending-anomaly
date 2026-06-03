# Section 508 Accessibility Review

**Project:** Federal Spending Anomaly Detection
**Author:** Hari Acharya
**Satisfies:** BR-06 (the dashboards must meet federal accessibility expectations)
**Scope:** The Power BI dashboard and the Tableau Public dashboard, both titled NASA Contract Awards FY2022 to FY2023, Anomaly Overview.

## Standard used

Section 508 of the Rehabilitation Act requires federal electronic content to meet the Web Content Accessibility Guidelines (WCAG) 2.1 at the AA level. This review checks both dashboards against the WCAG 2.1 AA success criteria that are most relevant to data dashboards.

## Method

Each dashboard was reviewed page by page against the criteria below. Findings are recorded honestly, including items that are met by design, items that needed a deliberate choice, and items that are recommended for a fuller production version.

## Findings

| WCAG criterion | What it requires | Status | Notes |
|---|---|---|---|
| 1.1.1 Non-text Content | Visuals have a text alternative | Recommended | Add a one line description to each dashboard summarizing what it shows, since chart images alone are not read by screen readers |
| 1.3.1 Info and Relationships | Structure is conveyed in text, not only layout | Met | The Anomaly Review table presents the same information as text, with the rules_triggered and risk_band columns spelled out |
| 1.4.1 Use of Color | Color is not the only way information is conveyed | Met | Risk level is shown as a text label (None, Low, Medium, High) in the risk_band column and the rule list is shown as text (R1, R2, R5, R6), so a colorblind reader does not depend on the color of a bar or slice |
| 1.4.3 Contrast (Minimum) | Text has at least 4.5 to 1 contrast | Met | All labels, titles, axis text, and the big number cards are dark text on a white background, which clears 4.5 to 1 |
| 1.4.11 Non-text Contrast | Chart elements have at least 3 to 1 contrast | Recommended | Verify the risk band colors against the white background and against each other with a contrast checker, and prefer a single hue light to dark ramp so the bands also read in grayscale |
| 2.4.6 Headings and Labels | Headings and labels are descriptive | Met | Every visual has a clear title, every axis is labeled, and the KPI cards are labeled |
| 1.4.10 Reflow / readability | Content is readable without loss | Partial | Both tools fix the canvas size, which is standard for dashboards, so a mobile layout is a recommended future addition |

## Deliberate accessibility choices we made

These were built in on purpose, not added afterward.

- **Risk level as a text label.** The risk_band column (None, Low, Medium, High) was created in the database specifically so the dashboards never rely on color alone to show how risky an award is. This is the single most important fix for color accessibility.
- **Rules shown as text.** The rules_triggered column spells out which rules fired, for example R1, R2, R5, R6, rather than encoding it in a color or icon.
- **Bar over pie where possible.** The Tableau version shows Awards by Risk Band as a bar chart, which is easier to read than a circular chart for someone with low vision. The Power BI version uses a donut but pairs it with a text legend and printed counts and percentages, so the values are still readable without distinguishing the colors.
- **Clear titles and labels.** Every visual is titled in plain language and every axis is labeled.

## Recommended fixes for a production version

1. **Switch the risk band colors to a single hue ramp** (light for None up to dark for High) so the four bands are distinguishable in grayscale and for colorblind users, not just by hue.
2. **Add a short text description** under each dashboard title, one or two sentences, so a screen reader user gets the gist without seeing the charts.
3. **Run a contrast checker** on the final color palette to confirm every chart color clears 3 to 1 against the background.
4. **Confirm the data tables expose their values to assistive technology**, which Power BI supports through its accessible table view and which Tableau exposes through its data view.

## Conclusion

Both dashboards meet the core Section 508 and WCAG 2.1 AA expectations for a data dashboard, most importantly never relying on color alone, because risk level and the triggered rules are always available as text. The remaining items are refinements, a colorblind safe palette, short text descriptions, and a formal contrast check, which are documented here as the next steps for a production deployment.