import requests, uuid
from datetime import datetime
from .common import standardise
from ..config import GREENHOUSE_TEMPLATE, COMPANIES


def fetch():
    out = []
    for slug in COMPANIES:
        try:
            r = requests.get(GREENHOUSE_TEMPLATE.format(slug=slug), timeout=10)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"[greenhouse] {slug}: {e}")
            continue

        for j in data.get("jobs", []):
            posted_raw = j.get("updated_at") or j.get("created_at") or datetime.utcnow().isoformat()
            out.append(
                standardise(
                    id_=j.get("id") or uuid.uuid4(),
                    company=slug.capitalize(),
                    title=j.get("title", "").strip(),
                    location=(j.get("location") or {}).get("name", ""),
                    url=j.get("absolute_url") or f"https://boards.greenhouse.io/{slug}/{j.get('id')}",
                    posted=posted_raw
                )
            )
    return out
