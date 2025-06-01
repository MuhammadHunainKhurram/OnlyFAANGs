import os
from dotenv import load_dotenv

load_dotenv()

# Backend database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./jobs.db")

# Google Jobs API
GOOGLE_API = os.getenv("GOOGLE_API", "https://careers.google.com/api/v3/search/")

# Greenhouse boards
GREENHOUSE_TEMPLATE = os.getenv(
    "GREENHOUSE_TEMPLATE",
    "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
)
COMPANIES = os.getenv("GREENHOUSE_COMPANIES", "").split(",") or [
    "airtable", "brex", "databricks", "discord",
    "duolingo", "figma", "notion", "scaleai",
    "samsara", "verkada", "whatnot"
]

# Amazon API
AMAZON_SEARCH_URL = os.getenv("AMAZON_SEARCH_URL", "https://www.amazon.jobs/en/search.json")
