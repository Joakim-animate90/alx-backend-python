"""
1. With DB Connection Decorator
This module provides a decorator that automatically opens and closes a sqlite3 database connection.
The connection is passed as the first argument to the decorated function.
"""

import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator that opens a sqlite3 in-memory database connection,
    passes it as the first argument to the decorated function,
    and ensures the connection is closed after the function finishes.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(":memory:")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Example usage:
if __name__ == "__main__":
    @with_db_connection
    def create_table_and_insert(conn):
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        print(result)

    # pylint: disable=no-value-for-parameter
    create_table_and_insert()
