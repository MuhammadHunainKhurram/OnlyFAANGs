from .amazon import fetch as amazon_fetch
from .google import fetch as google_fetch
from .greenhouse import fetch as greenhouse_fetch

__all__ = ["amazon_fetch", "google_fetch", "greenhouse_fetch"]
