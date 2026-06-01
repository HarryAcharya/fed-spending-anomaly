"""
ingest_awards.py
Phase 2, Step 10. Full ingestion of federal prime contract awards.

What this script does:
  1. Asks the API how many GSA contract awards exist for our window,
     so we know the size before we pull anything.
  2. Walks through the window one month at a time, from October 2021
     through September 2023 (fiscal years 2022 and 2023).
  3. Pages through each month, since a single query can only return
     up to 10,000 records and monthly slices stay under that.
  4. Retries automatically if the API is slow or returns a temporary error.
  5. Removes duplicate awards using their permanent ID.
  6. Saves everything to data/awards_raw.csv.

Run from the project folder with the venv active:
    python python/ingest_awards.py
"""

import csv
import time
import calendar
from datetime import date

import requests

# ---------------------------------------------------------------------------
# Settings. These are the only things you would change to adjust the pull.
# ---------------------------------------------------------------------------

SEARCH_URL = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
COUNT_URL = "https://api.usaspending.gov/api/v2/search/spending_by_award_count/"

# The agency we are pulling. This is the official top tier name.
AGENCY_NAME = "National Aeronautics and Space Administration"

# The window. Fiscal year 2022 starts October 2021. Fiscal year 2023 ends
# September 2023. So the full window is October 2021 through September 2023.
WINDOW_START = date(2021, 10, 1)
WINDOW_END = date(2023, 9, 30)

# A, B, C, D are the four prime contract award types.
AWARD_TYPE_CODES = ["A", "B", "C", "D"]

# The columns we ask for. The API also returns a few extra useful fields
# on its own, such as the permanent award ID we use to remove duplicates.
FIELDS = [
    "Award ID",
    "Recipient Name",
    "Award Amount",
    "Start Date",
    "End Date",
    "Awarding Agency",
    "Awarding Sub Agency",
    "Award Type",
    "Funding Agency",
    "Funding Sub Agency",
    "NAICS",
    "PSC",
]

OUTPUT_PATH = "data/awards_raw.csv"

# The API returns at most 100 records per page.
PAGE_SIZE = 100

# A short pause between calls so we are polite to a free public service.
PAUSE_SECONDS = 0.3


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_filters(start_date, end_date):
    """Build the filter block the API expects for one date window."""
    return {
        "award_type_codes": AWARD_TYPE_CODES,
        "agencies": [
            {"type": "awarding", "tier": "toptier", "name": AGENCY_NAME}
        ],
        "time_period": [
            {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            }
        ],
    }


def post_with_retries(url, payload, max_retries=4):
    """
    Send a POST request and retry on temporary problems.

    Returns the response object on success. If every attempt fails, or the
    API returns an error it will not recover from, it prints what happened
    and returns None so the caller can stop cleanly.
    """
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, json=payload, timeout=120)
        except requests.exceptions.RequestException as error:
            wait = attempt * 5
            print("   network problem, attempt", attempt, "-", error)
            print("   waiting", wait, "seconds then trying again")
            time.sleep(wait)
            continue

        if response.status_code == 200:
            return response

        # These status codes usually mean "busy, try again shortly".
        if response.status_code in (429, 500, 502, 503, 504):
            wait = attempt * 5
            print("   API returned", response.status_code,
                  "- waiting", wait, "seconds then trying again")
            time.sleep(wait)
            continue

        # Any other status is something we will not recover from by retrying,
        # such as a bad field name. Show the message and stop.
        print("   API returned an error it will not recover from:")
        print("   status", response.status_code)
        print("   message:", response.text[:1000])
        return None

    print("   gave up after", max_retries, "attempts")
    return None


def month_windows(start, end):
    """Yield (first_day, last_day) for each calendar month in the range."""
    year = start.year
    month = start.month
    while date(year, month, 1) <= end:
        last_day_number = calendar.monthrange(year, month)[1]
        first_day = date(year, month, 1)
        last_day = date(year, month, last_day_number)
        # Do not run past the overall end date.
        if last_day > end:
            last_day = end
        yield first_day, last_day
        # Move to the next month.
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1


def get_total_count():
    """Ask the API how many contract awards match, before we pull them."""
    payload = {"filters": build_filters(WINDOW_START, WINDOW_END),
               "spending_level": "awards"}
    response = post_with_retries(COUNT_URL, payload)
    if response is None:
        return None
    results = response.json().get("results", {})
    # For award types A, B, C, D the relevant bucket is "contracts".
    return results.get("contracts")


def pull_one_month(first_day, last_day):
    """Page through one month and return a list of award records."""
    month_records = []
    page = 1
    while True:
        payload = {
            "filters": build_filters(first_day, last_day),
            "fields": FIELDS,
            "spending_level": "awards",
            "subawards": False,
            "limit": PAGE_SIZE,
            "page": page,
        }
        response = post_with_retries(SEARCH_URL, payload)
        if response is None:
            print("   stopping this month early because of an API error")
            break

        results = response.json().get("results", [])
        month_records.extend(results)

        # A short page means we have reached the end of this month.
        if len(results) < PAGE_SIZE:
            break

        page += 1
        # Safety stop. 100 pages times 100 records is the 10,000 ceiling.
        if page > 100:
            print("   reached the 10,000 record ceiling for this month")
            break

        time.sleep(PAUSE_SECONDS)

    return month_records


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Federal Spending Anomaly Detection - data ingestion")
    print("Agency:", AGENCY_NAME)
    print("Window:", WINDOW_START.isoformat(), "to", WINDOW_END.isoformat())
    print()

    print("Step 1: asking the API how many contract awards match...")
    total = get_total_count()
    if total is None:
        print("Could not get a count. Stopping so we can look at the error.")
        return
    print("The API reports", total, "matching contract awards.")
    print()

    print("Step 2: pulling the data one month at a time...")
    # We store awards in a dictionary keyed by their permanent ID, which
    # removes duplicates automatically as we go.
    awards_by_id = {}
    duplicates = 0

    for first_day, last_day in month_windows(WINDOW_START, WINDOW_END):
        records = pull_one_month(first_day, last_day)
        new_this_month = 0
        for record in records:
            key = (record.get("generated_internal_id")
                   or record.get("internal_id")
                   or record.get("Award ID"))
            if key in awards_by_id:
                duplicates += 1
            else:
                new_this_month += 1
            awards_by_id[key] = record
        print("  ", first_day.isoformat(), "to", last_day.isoformat(),
              "->", len(records), "pulled,", new_this_month, "new")

    all_awards = list(awards_by_id.values())
    print()
    print("Pull complete.")
    print("Unique awards collected:", len(all_awards))
    print("Duplicates removed along the way:", duplicates)
    print()

    if not all_awards:
        print("No records collected, so nothing was written.")
        return

    print("Step 3: writing to", OUTPUT_PATH)
    # Build the full set of column names across every record, so no field
    # is lost even if some records carry extra keys.
    all_keys = set()
    for award in all_awards:
        all_keys.update(award.keys())
    # Put the fields we asked for first, then any extras the API added.
    ordered_keys = [f for f in FIELDS if f in all_keys]
    extras = sorted(k for k in all_keys if k not in FIELDS)
    fieldnames = ordered_keys + extras

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for award in all_awards:
            writer.writerow(award)

    print("Done. Wrote", len(all_awards), "rows to", OUTPUT_PATH)


if __name__ == "__main__":
    main()
