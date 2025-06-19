# app/scrapers/microsoft.py
import requests, datetime
from .common import standardise

SEARCH_URL = "https://gcsservices.careers.microsoft.com/search/api/v1/search"

# default query parameters (students + US internships) – tweak later via env-vars if you like
DEFAULT_PARAMS = {
    "lc":   "United States",              # location-country filter
    "exp":  "Students and graduates",     # experience filter
    "l":    "en_us",                      # locale
    "pg":   1,                            # page
    "pgSz": 20,                           # page size (max 20 permitted)
    "o":    "Recent",                     # order
    "flt":  "true"                        # “true” = apply filters
}

def fetch():
    out = []

    # Pull first 3 pages (60 jobs) – Microsoft paginates by "pg"
    for page in (1, 2, 3):
        params = {**DEFAULT_PARAMS, "pg": page}
        try:
            r = requests.get(SEARCH_URL, params=params, timeout=10)
            r.raise_for_status()
            jobs = (r.json()
                      .get("operationResult", {})
                      .get("result", {})
                      .get("jobs", []))
        except Exception as e:
            print("[microsoft] page", page, "failed:", e)
            continue

        for j in jobs:
            props = j.get("properties", {})
            job_id   = j.get("jobId")
            title    = j.get("title", "").strip()
            location = props.get("primaryLocation", "Various")
            url      = f"https://jobs.careers.microsoft.com/global/en/job/{job_id}"

            raw_date = j.get("postingDate")              # e.g. "2025-06-03T12:04:21.000Z"
            try:
                posted = datetime.datetime.fromisoformat(raw_date.rstrip("Z"))
            except Exception:
                posted = datetime.datetime.utcnow()

            out.append(
                standardise(
                    id_=job_id,
                    company="Microsoft",
                    title=title,
                    location=location,
                    url=url,
                    posted=posted,
                )
            )

    return out
