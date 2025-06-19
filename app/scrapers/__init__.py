from .amazon      import fetch as amazon_fetch
from .google      import fetch as google_fetch
from .greenhouse  import fetch as greenhouse_fetch
from .lever       import fetch as lever_fetch
from .microsoft   import fetch as microsoft_fetch

SCRAPER_FUNCS = [
    amazon_fetch,
    google_fetch,
    greenhouse_fetch,
    lever_fetch,
    microsoft_fetch,
]
