import time

def timeit(method):
    """Decorator to measure execution time of a method"""
    def timed(*args, **kw):
        start_time = time.time()
        result = method(*args, **kw)
        end_time = time.time()
        print(f"Method {method.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return timed