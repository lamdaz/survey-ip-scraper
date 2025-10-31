import time
import functools
import logging
from typing import Callable

logger = logging.getLogger(__name__)

def rate_limited(max_per_second: float):
    """Simple rate limiter decorator."""
    min_interval = 1.0 / float(max_per_second)
    def decorate(func: Callable):
        last_time = {"t": 0.0}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_time["t"]
            wait = min_interval - elapsed
            if wait > 0:
                time.sleep(wait)
            result = func(*args, **kwargs)
            last_time["t"] = time.time()
            return result
        return wrapper
    return decorate

def safe_get(d, *keys, default=""):
    for k in keys:
        if not d:
            return default
        d = d.get(k, default)
    return d or default
