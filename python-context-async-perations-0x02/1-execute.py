"""
1. ExecuteQuery Context Manager
This module provides a class-based context manager that takes a query and parameters,
executes the query, and returns the result, managing both the connection and query execution.
"""

import sqlite3

class ExecuteQuery:
    """
    Context manager that opens a sqlite3 connection, executes a query with parameters,
    and returns the result.
    """
    def __init__(self, query, params=None, db_path=":memory:"):
        self.query = query
        self.params = params if params is not None else ()
        self.db_path = db_path
        self.conn = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        # For demonstration, create table and insert data
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 22))
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Carol", 27))
        self.conn.commit()
        # Execute the provided query
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

# Example usage:
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)
    with ExecuteQuery(query, param) as results:
        print(results)
