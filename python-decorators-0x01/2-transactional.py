"""
2. Transactional Decorator
This module provides:
- with_db_connection: a decorator that opens and closes a sqlite3 database connection.
- transactional: a decorator that wraps a function in a database transaction, committing on success and rolling back on error.
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

def transactional(func):
    """
    Decorator that wraps a function in a database transaction.
    Commits if the function completes successfully, rolls back if an exception occurs.
    Assumes the first argument is a sqlite3 connection.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise
    return wrapper

# Example usage:
if __name__ == "__main__":
    @with_db_connection
    @transactional
    def create_and_insert(conn):
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

    @with_db_connection
    @transactional
    def fail_insert(conn):
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        # This will fail (NULL constraint violation)
        cursor.execute("INSERT INTO users (name) VALUES (NULL)")
        return cursor.fetchall()

    # pylint: disable=no-value-for-parameter
    print("Successful transaction:", create_and_insert())
    try:
        print("Failed transaction:", fail_insert())
        fail_insert()
    except Exception as e:
        print("Transaction failed and rolled back:", e)
