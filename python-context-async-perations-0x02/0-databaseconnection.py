"""
0. DatabaseConnection Context Manager
This module provides a class-based context manager for handling opening and closing
a sqlite3 database connection automatically.
"""

import sqlite3

class DatabaseConnection:
    """
    Context manager for sqlite3 database connections.
    Opens the connection on entry and closes it on exit.
    """
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

# Example usage:
if __name__ == "__main__":
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        # Create table and insert data for demonstration
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))
        conn.commit()

        # Now perform the required query
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
