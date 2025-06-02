from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from .database import SessionLocal
from .models import Job
from .scrapers import amazon_fetch, google_fetch, greenhouse_fetch

SCRAPER_FUNCS = [amazon_fetch, google_fetch, greenhouse_fetch]

def ingest():
    db = SessionLocal()
    existing_ids = {row[0] for row in db.query(Job.id).all()}
    seen_ids = set(existing_ids)
    added = 0

    try:
        for func in SCRAPER_FUNCS:
            for job in func():
                jid = job["id"]
                if jid in seen_ids:
                    continue
                seen_ids.add(jid)
                db.add(Job(**job))
                added += 1

        db.commit()
    except IntegrityError:
        db.rollback()
    finally:
        db.close()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] ingest ran – {added} new rows")

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(ingest, "interval", minutes=15)
scheduler.start()
