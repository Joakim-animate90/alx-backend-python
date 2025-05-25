#!/usr/bin/env python3

from seed import connect_to_prodev
from mysql.connector import Error

def paginate_users(page_size, offset):
    """
    Fetch a page of users from the user_data table starting at the given offset.

    Args:
        page_size (int): Number of records per page.
        offset (int): Offset to start fetching records from.

    Returns:
        list: A list of user records (dicts) for the page.
    """
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    connection = connect_to_prodev()
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (page_size, offset))
            return cursor.fetchall()
    except Error as e:
        print(e)
        return []
    finally:
        connection.close()

def lazy_paginate(page_size):
    """
    Generator that lazily fetches and yields users page by page.

    Args:
        page_size (int): Number of records per page.

    Yields:
        dict: User records from the database.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        for user_record in page:
            yield user_record
        offset += page_size

if __name__ == "__main__":
    # Example usage: print all users in pages of 5
    for user in lazy_paginate(5):
        print(user)
