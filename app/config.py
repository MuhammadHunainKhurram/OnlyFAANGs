import os
from dotenv import load_dotenv

load_dotenv()

# Backend database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./jobs.db")


# Google API
GOOGLE_API = os.getenv("GOOGLE_API", "https://careers.google.com/api/v3/search/")


# Greenhouse API
GREENHOUSE_TEMPLATE = os.getenv(
    "GREENHOUSE_TEMPLATE",
    "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
)
GREENHOUSE_COMPANIES = [c for c in os.getenv("GREENHOUSE_COMPANIES", "").split(",") if c]


# Amazon API
AMAZON_SEARCH_URL = os.getenv("AMAZON_SEARCH_URL", "https://www.amazon.jobs/en/search.json")


# Lever API
LEVER_TEMPLATE = os.getenv(
    "LEVER_TEMPLATE",
    "https://api.lever.co/v0/postings/{slug}?mode=json"
)
LEVER_COMPANIES = [c for c in os.getenv("LEVER_COMPANIES", "").split(",") if c]