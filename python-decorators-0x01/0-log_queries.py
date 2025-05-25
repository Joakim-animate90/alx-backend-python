#!/usr/bin/env python3

"""
0x01. Log SQL Queries
This module provides a decorator to log SQL queries before executing a function.
"""

import functools
import sqlite3
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
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{now}] Executing SQL query: {args[0]}")
            return func(*args, **kwargs)

        return wrapper

    return decorator

@log_queries()
def execute_query(query, db_path=':memory:'):
    """
    Executes a SQL query on the specified SQLite database.

    Args:
        query (str): The SQL query to execute.
        db_path (str): Path to the SQLite database file. Defaults to in-memory database.

    Returns:
        list: Result of the query execution.
    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result
if __name__ == "__main__":
    # Example usage
    query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)"
    execute_query(query)
