import time
from functools import wraps

def trace_step(name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = round(time.time() - start, 3)

            print(f"[TRACE] {name} completed in {duration}s")
            return result
        return wrapper
    return decorator