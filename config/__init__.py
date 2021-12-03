from functools import lru_cache
import os


@lru_cache
def get_settings():
    if os.environ.get("DEBUG"):
        from .dev import Settings
    else:
        from .base import Settings
    return Settings()
