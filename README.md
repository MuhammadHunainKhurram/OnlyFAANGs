````markdown
# OnlyFAANGs — 24 × 7 Job-Scraping & Notification Pipeline  
*A cloud-hosted FastAPI service + Chrome extension that tracks tech-company roles in real time.*

<p align="center">
  <img src="docs/architecture.svg" width="640" alt="High-level architecture diagram"/>
</p>

---

## ⚡️ Why it Exists
Searching every big-tech career site daily is soul-crushing and error-prone. **OnlyFAANGs** automates that grind:

| Feature | Details |
|---------|---------|
| **Real-time scraping** | Amazon, Google, and any Greenhouse boards you list (Airtable, Figma, etc.). |
| **Canonical data model** | Company-agnostic shape → single endpoint → easy for any client. |
| **24 × 7 hosted** | Docker container on **AWS Elastic Beanstalk** + **RDS PostgreSQL** → keeps ingesting even when your laptop is closed. |
| **Instant desktop alerts** | Manifest V3 Chrome extension polls every 15 min, badges new jobs with 🔴 dots, and fires `chrome.notifications`. |
| **“Apply” checkbox** | Tick a job → persisted in `chrome.storage` so you never double-apply. |
| **Environment-variable driven** | No secrets or hard-coded URLs in the repo. |
| **Plug-and-play scrapers** | Drop `scrapers/leverd.py` tomorrow—one import line and scheduler picks it up. |

---

## 🧩 Full Stack Overview

| Layer | Tech | Why chosen |
|-------|------|-----------|
| **Browser UI** | Chrome Extension (MV3) + HTML/CSS/JS | No install friction; lives next to your tabs; instant notifications. |
| **API** | **FastAPI** + Uvicorn | Async, type-hinted, OpenAPI docs out of the box. |
| **Scheduler** | **APScheduler** | In-process cron that survives container restarts; no Celery overhead. |
| **Scrapers** | Python `requests` modules | Simple, stateless, easy to expand. |
| **ORM / DB** | **SQLAlchemy 2** → **PostgreSQL (RDS free tier)** | One model, swap DBs at will. |
| **Container** | **Docker** (`python:3.11-slim`) | “Works on my machine” everywhere, including AWS. |
| **Hosting** | **AWS Elastic Beanstalk – single t3.micro** | One-command deploy, health checks, log aggregation. |
| **Secrets** | `.env` + `python-dotenv` + EB env vars | Never commit creds; EB gets them at runtime. |

---

## 🚀 Quick Start (local dev)

```bash
git clone https://github.com/YOUR_USERNAME/OnlyFAANGs.git
cd OnlyFAANGs

# 1️⃣  Prereqs
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2️⃣  Secrets (never commit)
cp .env.example .env          # edit DATABASE_URL / API endpoints

# 3️⃣  Run back-end locally
uvicorn app.main:app --reload

# 4️⃣  Load the Chrome extension
chrome://extensions  →  “Load unpacked” →  ./extension

# Boom: http://127.0.0.1:8000/jobs/latest?limit=10
````

> **Want Docker instead?**
>
> ```bash
> docker build -t onlyfaangs .
> docker run -p 8080:8080 --env-file .env onlyfaangs
> ```

---

## ☁️ One-Click Cloud Deploy (AWS Elastic Beanstalk)

```bash
# Prereqs: AWS CLI + EB CLI + RDS Postgres already created

eb init -p docker onlyfaangs --region us-east-1
eb setenv DATABASE_URL='postgresql+psycopg2://user:pass@host:5432/db'
eb create onlyfaangs-env --single --instance_type t3.micro
eb open   # view live API
```

> After code changes:
>
> ```bash
> git commit -am "feat: new scraper"
> eb deploy
> ```

---

## 🗂 Important Directories

```
app/
 ├─ config.py          # all URLs & env lookups
 ├─ main.py            # FastAPI entrypoint
 ├─ scheduler.py       # APScheduler glue
 ├─ scrapers/          # amazon.py, google.py, greenhouse.py, …
 └─ models.py          # SQLAlchemy ORM

extension/
 ├─ manifest.json
 ├─ config.js          # API_URL (git-ignored)
 ├─ popup.html/css/js
 └─ service-worker.js

Dockerfile             # build + EXPOSE 8080
.env.example           # sample secrets template
```

---

## 🔌 Adding a New Scraper in 3 Steps

```python
# app/scrapers/leverd.py
import requests, uuid, datetime
from ..common import standardise

API = "https://api.lever.co/v0/postings/<company>?mode=json"

def fetch():
    rows = requests.get(API, timeout=10).json()
    return [
        standardise(
            id_      = r["id"],
            company  = "<Company>",
            title    = r["text"],
            location = r["categories"]["location"],
            url      = r["hostedUrl"],
            posted   = datetime.datetime.fromtimestamp(r["createdAt"]/1000),
        )
        for r in rows
    ]
```

1. **Drop file →** `app/scrapers/leverd.py`
2. **export** it in `scrapers/__init__.py`
3. **append** it to `SCRAPER_FUNCS` in `scheduler.py` → redeploy.

No code elsewhere changes.

---

## 🔒 Security

| Risk                   | Mitigation                                                                    |
| ---------------------- | ----------------------------------------------------------------------------- |
| Secrets in repo        | `.env`, `extension/config.js` in `.gitignore`; CI will fail if secrets found. |
| DB exposed to internet | RDS SG restricts port 5432 to EB SG only.                                     |
| HTTPS                  | Add ACM cert + EB load balancer (5 min wizard).                               |
| API hammering          | FastAPI dependency injection → plug in API key or IP rate-limit later.        |

---

## 🛤 Roadmap

* [ ] Lever / Workday scraper modules
* [ ] Slack or Discord webhook notifier
* [ ] React admin dashboard (stats, filters, resend notifications)
* [ ] GitHub Actions CI → automated `eb deploy` on `main`
* [ ] Docker Compose for local dev (Postgres + app)

---

## 🤝 Contributing

1. Fork → create branch → PR.
2. Run `make lint` and `make test` (coming soon).
3. One small feature per PR.

---

## 📜 License

MIT — do anything, give credit, no warranty.

---

> **Built by Muhammad Hunain Khurram** —
> because applying to tech companies should be easier than getting the job itself.

````

---

### How to use it

1. Save the block above as **`README.md`** in your repo root.  
2. Replace image placeholders (`docs/architecture.svg`) with your own diagram or remove.  
3. Swap `YOUR_USERNAME` and the example EB URL with your real values.  
4. Commit and push:

```bash
git add README.md
git commit -m "docs: first public README"
git push
````
