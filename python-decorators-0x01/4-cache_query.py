"""
4. Cache Query Decorator
This module provides a cache_query decorator that caches the results of database queries
based on the SQL query string to avoid redundant calls.
"""

import functools

def cache_query(func):
    """
    Decorator that caches the results of database queries based on the SQL query string.
    Assumes the SQL query is the first argument to the function.
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not args:
            return func(*args, **kwargs)
        query = args[0]
        if query in cache:
            print(f"Cache hit for query: {query}")
            return cache[query]
        print(f"Cache miss for query: {query}")
        result = func(*args, **kwargs)
        cache[query] = result
        return result

    return wrapper

# Example usage:
if __name__ == "__main__":
    call_counter = {"count": 0}

    @cache_query
    def execute_query(query):
        call_counter["count"] += 1
        # Simulate a database call
        return f"Result for: {query}"

    print(execute_query("SELECT * FROM users"))
    print(execute_query("SELECT * FROM users"))  # Should hit cache
    print(execute_query("SELECT * FROM orders"))
    print(execute_query("SELECT * FROM users"))  # Should hit cache again
    print(f"Actual DB calls: {call_counter['count']}")
