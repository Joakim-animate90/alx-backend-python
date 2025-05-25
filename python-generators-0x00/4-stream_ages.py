#!/usr/bin/env python3

from seed import connect_to_prodev
from mysql.connector import Error

def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    query = "SELECT age FROM user_data"
    connection = connect_to_prodev()
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            for row in cursor:
                age = row.get("age")
                if age is not None:
                    yield age
    except Error as e:
        print(e)
    finally:
        connection.close()

def compute_average_age():
    """
    Computes the average age of users using the stream_user_ages generator.
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    average = total / count if count > 0 else 0
    print(f"Average age of users: {average}")

if __name__ == "__main__":
    compute_average_age()
