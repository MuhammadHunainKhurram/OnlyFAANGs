import requests
from datetime import datetime
from .common import standardise
from ..config import LEVER_COMPANIES, LEVER_TEMPLATE

def fetch():
    out = []
    for slug in LEVER_COMPANIES:
        try:
            resp = requests.get(LEVER_TEMPLATE.format(slug=slug), timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"[lever] error fetching from {slug}:", e)
            continue

        for job in resp.json():
            out.append(
                standardise(
                    id_=job["id"],
                    company=slug.capitalize(),
                    title=job["text"],
                    location=job["categories"].get("location", "N/A"),
                    url=job["hostedUrl"],
                    posted=datetime.fromtimestamp(job["createdAt"] / 1000)
                )
            )
    return out
