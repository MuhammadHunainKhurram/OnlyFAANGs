from datetime import datetime

def standardise(id_, company, title, location, url, posted):
    if isinstance(posted, str):
        posted = datetime.fromisoformat(posted.rstrip("Z"))

    return {
        "id":       str(id_),
        "company":  company,
        "title":    title,
        "location": location,
        "url":      url,
        "posted":   posted,
    }
