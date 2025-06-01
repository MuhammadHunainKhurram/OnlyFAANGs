from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, Job
from .scheduler import ingest  # ensures scheduler starts on import

# auto-create tables on first run
Base.metadata.create_all(bind=engine)

app = FastAPI(title="JobWatch API")

def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def bootstrap():
    # grab initial data immediately
    ingest()

@app.get("/jobs/latest")
def latest(limit: int = 100, db: Session = Depends(db_session)):
    rows = (
        db.query(Job)
          .order_by(Job.posted.desc())
          .limit(limit)
          .all()
    )
    # SQLAlchemy Rows → plain dicts (and ISO-8601 dates for JSON)
    return [
        {
            **r.__dict__,
            "posted": r.posted.isoformat()
        } for r in rows
    ]
