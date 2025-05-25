#!/usr/bin/env python3

from mysql.connector import Error
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of user records from the user_data table.

    Args:
        batch_size (int): Number of records per batch.

    Yields:
        list: A list of user records (dicts) in each batch.
    """
    query = "SELECT * FROM user_data"
    connection = connect_to_prodev()
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch
    except Error as e:
        print(e)
    finally:
        connection.close()
    return

def batch_processing(batch_size):
    """
    Processes each batch of users, yielding users over the age of 25.

    Args:
        batch_size (int): Number of records per batch.

    Yields:
        dict: User records where age > 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user.get("age", 0) > 25:
                yield user
    return

if __name__ == "__main__":
    # Example usage: print users over 25 in batches of 10
    for user_record in batch_processing(10):
        print(user_record)
