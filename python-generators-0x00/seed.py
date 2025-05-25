#!/usr/bin/env python3
"""Seed script for initializing and populating the ALX_prodev MySQL database."""

# If you see "Import 'mysql.connector' could not be resolved" or "Unable to import 'mysql.connector'",
# make sure your VSCode is using the correct Python interpreter (the one where mysql-connector-python is installed).
# In VSCode, press Ctrl+Shift+P, type "Python: Select Interpreter", and choose the interpreter from your virtual environment.
# You can verify the package is installed by running: pip show mysql-connector-python

from mysql.connector import connect, Error

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'password'
DB_NAME = 'ALX_prodev'

def connect_db():
    """Connect to the MySQL database using provided credentials.

    Returns:
        MySQLConnection: Connection object if successful, None otherwise.
    """
    try:
        return connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    except Error as e:
        print(e)
        return None


def create_database(connection):
    """Create the database if it does not already exist.

    Args:
        connection (MySQLConnection): The MySQL connection object.
    """
    query = f'CREATE DATABASE IF NOT EXISTS {DB_NAME}'
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
    except Error as e:
        print(e)


def connect_to_prodev():
    """Connect to the MySQL database with the specified database name.

    Returns:
        MySQLConnection: Connection object if successful, None otherwise.
    """
    try:
        return connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    except Error as e:
        print(e)
        return None


def create_table(connection):
    """Create the user_data table if it does not already exist.

    Args:
        connection (MySQLConnection): The MySQL connection object.
    """
    query = '''CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(255) PRIMARY KEY, 
                name VARCHAR(255) NOT NULL, 
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )'''
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
    except Error as e:
        print(e)


def insert_data(connection, data):
    """Insert a new user record into the user_data table.

    Args:
        connection (MySQLConnection): The MySQL connection object.
        data (dict): Dictionary containing user data with keys 'uuid', 'name', 'email', and 'age'.
    """
    query = f'''
            INSERT INTO user_data VALUES
            ("{data['uuid']}", "{data['name']}", "{data['email']}", {data['age']})
            '''
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
    except Error as e:
        print(e)


if __name__ == '__main__':
    conn1 = connect_db()
    create_database(conn1)
    conn2 = connect_to_prodev()
    create_table(conn2)
    insert_data(conn2,
        {
            "uuid": "2cb9e2c9-bc99-4ed0-b203-4c7f35733578",
            "name": "Joakim Bwire",
            "email": "joakimbwire@example.com",
            "age": 24
        }
    )
    conn1.close()
    conn2.close()
