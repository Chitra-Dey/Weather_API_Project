import time

CACHE = {}

def get_from_cache(key: str):
    data = CACHE.get(key)
    if not data:
        return None
    value, expiry = data
    if expiry < time.time(): 
        del CACHE[key]
        return None
    return value

def set_in_cache(key: str, value: dict, ttl: int = 300): #5 min 
    expiry = time.time() + ttl
    CACHE[key] = (value, expiry)
