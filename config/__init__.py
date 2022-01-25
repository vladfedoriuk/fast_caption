import os
from functools import lru_cache


@lru_cache
def get_settings():
    if os.environ.get("DEBUG"):
        from .dev import Settings
    elif os.environ.get("TEST"):
        from .test import Settings
    else:
        from .base import Settings
    return Settings()
