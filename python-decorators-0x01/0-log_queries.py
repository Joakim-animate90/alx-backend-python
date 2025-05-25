#!/usr/bin/env python3

"""
0x01. Log SQL Queries
This module provides a decorator to log SQL queries before executing a function.
"""

import functools
from datetime import datetime



def log_queries():
    """
    Decorator that logs the SQL query before executing the decorated function.
    Assumes the SQL query is the first argument to the function.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if args:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{now}] Executing SQL query: {args[0]}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
