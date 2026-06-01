"""
api_test.py
Phase 2, Step 9. A single test call to the USASpending award search API.

Purpose: confirm the API answers before we build the full ingestion script.
We are not saving anything here. We just want to see status 200 and a few
award records come back.

Run from the project folder with the venv active:
    python python/api_test.py
"""

import requests

URL = "https://api.usaspending.gov/api/v2/search/spending_by_award/"

payload = {
    "limit": 10,
    "page": 1,
    "subawards": False,
    "spending_level": "awards",
    "filters": {
        "award_type_codes": ["A", "B", "C", "D"],
        "time_period": [
            {"start_date": "2022-10-01", "end_date": "2023-09-30"}
        ],
    },
    "fields": [
        "Award ID",
        "Recipient Name",
        "Award Amount",
        "Awarding Agency",
        "Start Date",
    ],
}

print("Sending a test request to the USASpending API...")

try:
    response = requests.post(URL, json=payload, timeout=60)
except requests.exceptions.RequestException as error:
    print("The request could not be completed.")
    print("Error:", error)
    raise SystemExit(1)

print("Status code:", response.status_code)

if response.status_code != 200:
    print("The API did not return success. Here is what it said:")
    print(response.text)
    raise SystemExit(1)

data = response.json()
results = data.get("results", [])
print("Number of records returned:", len(results))

if results:
    print("\nFirst record returned:")
    for key, value in results[0].items():
        print("  ", key, "=", value)
else:
    print("The call worked but returned no records. We may need to widen the filter.")

print("\nTest complete.")
