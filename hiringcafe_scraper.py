"""
HiringCafe Job Scraper
----------------------
Fetches job listings for "Marketing Director" in New York (last 14 days)
and saves them into a CSV file using pandas.

Includes:
- url
- job title
- company
- salary range
- remote (yes/no)
- workplace_type
- location
- seniority level
- commitment
- apply_source
"""

import requests
import pandas as pd
import json

url = "https://hiring.cafe/api/search-jobs"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Base payload (from DevTools)
payload = {
    "size": 40,   # 40 jobs per page (max supported)
    "page": 0,    # will update in loop
    "searchState": {
        "locations": [
            {
                "id": "ZhY1yZQBoEtHp_8UErzY",
                "types": ["administrative_area_level_1"],
                "address_components": [
                    {"long_name": "New York", "short_name": "NY", "types": ["administrative_area_level_1"]},
                    {"long_name": "United States", "short_name": "US", "types": ["country"]}
                ],
                "formatted_address": "New York, United States",
                "population": 19274244,
                "workplace_types": [],
                "options": {
                    "flexible_regions": [
                        "anywhere_in_country",
                        "anywhere_in_continent",
                        "anywhere_in_world"
                    ]
                }
            }
        ],
        "workplaceTypes": ["Remote", "Hybrid", "Onsite"],
        "defaultToUserLocation": True,
        "userLocation": None,
        "searchQuery": "marketing director",
        "dateFetchedPastNDays": 14,
        "sortBy": "default"
    }
}

all_jobs = []
page = 0

while True:
    payload["page"] = page
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    if res.status_code != 200:
        print(f"-- Error {res.status_code} on page {page}")
        break

    data = res.json()
    results = data.get("results", [])

    if not results:  # stop if no more jobs
        break

    all_jobs.extend(results)
    print(f"-- Collected {len(results)} jobs from page {page}")
    page += 1

# Extract fields into a clean dataset
jobs_clean = []
for job in all_jobs:
    job_data = job.get("v5_processed_job_data", {})
    company_data = job.get("v5_processed_company_data", {})
    job_info = job.get("job_information", {})

    jobs_clean.append({
        "url": job.get("apply_url", ""),
        "job_title": job_info.get("title", ""),
        "company": job_data.get("company_name", company_data.get("name", "")),
        "salary_min": job_data.get("yearly_min_compensation", ""),
        "salary_max": job_data.get("yearly_max_compensation", ""),
        "remote": "yes" if str(job_data.get("workplace_type", "")).lower() == "remote" else "no",
        "workplace_type": job_data.get("workplace_type", ""),
        "location": job_data.get("formatted_workplace_location", ""),
        "seniority_level": job_data.get("seniority_level", ""),
        "commitment": ", ".join(job_data.get("commitment", [])),
        "apply_source": job.get("source", "")
    })

df = pd.DataFrame(jobs_clean)
df.to_csv("hiringcafe_jobs.csv", index=False, encoding="utf-8")

print(f"\n-- Finished! Saved {len(df)} total jobs to hiringcafe_jobs.csv")
