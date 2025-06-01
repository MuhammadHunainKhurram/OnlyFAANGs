import requests
from datetime import datetime
from .common import standardise
from ..config import AMAZON_SEARCH_URL


def fetch():
    params = {
        "country":    "USA",
        "job_type":   "Full-Time",      # flip to "Intern" etc. if needed
        "category":   "University",
        "base_query": "intern",
        "sort":       "recent",
    }

    out = []
    for offset in (0, 10, 20):
        try:
            resp = requests.get(AMAZON_SEARCH_URL,
                                params={**params, "offset": offset},
                                timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print("[amazon] request failed:", e)
            continue

        for j in resp.json().get("jobs", []):
            job_id = j.get("id_icims")
            if not job_id:
                continue

            out.append(
                standardise(
                    id_=job_id,
                    company="Amazon",
                    title=j["title"].strip(),
                    location=j.get("normalized_location") or j.get("location", ""),
                    url="https://www.amazon.jobs" + j["job_path"],
                    posted=datetime.strptime(j["posted_date"], "%B %d, %Y"),
                )
            )
    return out
