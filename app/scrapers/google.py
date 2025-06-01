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
    params = [
        ("category", "DATA_CENTER_OPERATIONS"),
        ("category", "DEVELOPER_RELATIONS"),
        ("category", "HARDWARE_ENGINEERING"),
        ("category", "INFORMATION_TECHNOLOGY"),
        ("category", "MANUFACTURING_SUPPLY_CHAIN"),
        ("category", "NETWORK_ENGINEERING"),
        ("category", "PRODUCT_MANAGEMENT"),
        ("category", "PROGRAM_MANAGEMENT"),
        ("category", "SOFTWARE_ENGINEERING"),
        ("category", "TECHNICAL_INFRASTRUCTURE_ENGINEERING"),
        ("category", "TECHNICAL_SOLUTIONS"),
        ("category", "TECHNICAL_WRITING"),
        ("category", "USER_EXPERIENCE"),

        ("location", "United States"),

        ("employment_type", "INTERN"),
        ("employment_type", "FULL_TIME"),
        ("employment_type", "PART_TIME"),
        ("employment_type", "TEMPORARY"),

        ("degree", "MASTERS"),
        ("degree", "BACHELORS"),
        ("degree", "PURSUING_DEGREE"),

        ("target_level", "INTERN_AND_APPRENTICE"),
        ("target_level", "EARLY"),

        ("sort_by", "date"),
    ]

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
