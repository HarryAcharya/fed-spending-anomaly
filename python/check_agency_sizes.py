"""
check_agency_sizes.py
A quick helper. It does NOT pull any data. It only asks the API how many
prime contract awards each candidate agency has for our window, so we can
pick one that lands in the tens of thousands.

Run from the project folder with the venv active:
    python python/check_agency_sizes.py
"""

import requests

COUNT_URL = "https://api.usaspending.gov/api/v2/search/spending_by_award_count/"

WINDOW_START = "2021-10-01"
WINDOW_END = "2023-09-30"
AWARD_TYPE_CODES = ["A", "B", "C", "D"]

# A short list of candidate agencies, smaller than GSA. Names are the
# official top tier names the API expects.
CANDIDATES = [
    "Environmental Protection Agency",
    "Small Business Administration",
    "National Science Foundation",
    "Department of Education",
    "Social Security Administration",
    "National Aeronautics and Space Administration",
]


def count_for(agency_name):
    payload = {
        "filters": {
            "award_type_codes": AWARD_TYPE_CODES,
            "agencies": [
                {"type": "awarding", "tier": "toptier", "name": agency_name}
            ],
            "time_period": [
                {"start_date": WINDOW_START, "end_date": WINDOW_END}
            ],
        },
        "spending_level": "awards",
    }
    try:
        response = requests.post(COUNT_URL, json=payload, timeout=60)
    except requests.exceptions.RequestException as error:
        return "request failed: " + str(error)
    if response.status_code != 200:
        return "error " + str(response.status_code) + ": " + response.text[:200]
    return response.json().get("results", {}).get("contracts")


def main():
    print("Counting prime contract awards per agency")
    print("Window:", WINDOW_START, "to", WINDOW_END)
    print("(target: an agency in the tens of thousands)")
    print()
    print(f"{'Agency':<48}{'Contract awards':>16}")
    print("-" * 64)
    for agency in CANDIDATES:
        count = count_for(agency)
        print(f"{agency:<48}{str(count):>16}")
    print()
    print("Done. Tell me which numbers came back and we will pick one.")


if __name__ == "__main__":
    main()
