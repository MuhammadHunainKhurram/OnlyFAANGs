import requests
from datetime import datetime
from .common import standardise
from ..config import GOOGLE_API

def _extract_id(raw_id: str | None) -> str | None:
    if not raw_id:
        return None
    parts = raw_id.split("/", 1)
    return parts[1] if len(parts) == 2 else None


def fetch():
    params = {
    "location":  "United States",
    "page_size": 20,
    "language_code": "en-US",
    "target_level": "INTERN_AND_APPRENTICE",
    "target_level": "EARLY",
    "order_by": "relevance desc"
    }

    try:
        res = requests.get(GOOGLE_API, params=params, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print("[google] request failed:", e)
        return []

    out = []
    for j in res.json().get("jobs", []):
        job_id = _extract_id(j.get("id"))
        if not job_id:
            continue

        title     = j.get("title", "").strip()
        locs      = j.get("locations", [])
        location  = locs[0]["display"] if locs else ""
        url       = j.get("apply_url") or f"https://careers.google.com/jobs/results/{job_id}/"

        posted_raw = (
            j.get("publish_date")
            or j.get("created")
            or j.get("modified")
            or datetime.utcnow().isoformat()
        )

        out.append(
            standardise(
                id_       = job_id,
                company   = "Google",
                title     = title,
                location  = location,
                url       = url,
                posted    = posted_raw,
            )
        )

    return out
