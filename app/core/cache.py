import time

cache_store = {}

CACHE_TTL = 300


def get_cached(key):
    entry = cache_store.get(key)

    if not entry:
        return None

    value, timestamp = entry

    if time.time() - timestamp > CACHE_TTL:
        cache_store.pop(key, None)
        return None

    return value


def set_cache(key, value):
    cache_store[key] = (value, time.time())