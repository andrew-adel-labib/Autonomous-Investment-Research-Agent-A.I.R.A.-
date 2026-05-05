import time

cache = {}


def set_cache(key, value, ttl=300):
    cache[key] = {
        "value": value,
        "expires": time.time() + ttl
    }


def get_cached(key):
    item = cache.get(key)

    if not item:
        return None

    if time.time() > item["expires"]:
        del cache[key]
        return None

    return item["value"]