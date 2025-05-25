# Python Generators: Batch Processing, Lazy Pagination, and Memory-Efficient Aggregation

This directory contains Python scripts demonstrating the use of generators for efficient data processing, including batch processing, lazy pagination, and memory-efficient aggregation from a database.

## Files and Descriptions

### 1. `1-batch_processing.py`
- **Purpose:** Processes user records in batches and yields users over the age of 25.
- **Key Functions:**
  - `stream_users_in_batches(batch_size)`: Generator that yields batches of user records from the database.
  - `batch_processing(batch_size)`: Yields users with age > 25 from each batch.
- **Usage:** Prints users over 25 in batches of 10.

### 2. `2-lazy_paginate.py`
- **Purpose:** Lazily fetches and yields user records page by page, simulating paginated database access.
- **Key Functions:**
  - `paginate_users(page_size, offset)`: Fetches a page of users from the database at a given offset.
  - `lazy_paginate(page_size)`: Generator that yields users one by one, fetching the next page only when needed.
- **Usage:** Prints all users in pages of 5.

### 3. `4-stream_ages.py`
- **Purpose:** Computes the average age of users in a memory-efficient way using a generator.
- **Key Functions:**
  - `stream_user_ages()`: Generator that yields user ages one by one from the database.
  - `compute_average_age()`: Uses the generator to calculate and print the average age without loading all data into memory.
- **Usage:** Prints the average age of users.

## Requirements

- Python 3.x
- MySQL database with a `user_data` table
- `mysql-connector-python` package
- Database connection details configured in `seed.py`

## How to Run

Each script can be run directly:
```bash
python3 1-batch_processing.py
python3 2-lazy_paginate.py
python3 4-stream_ages.py
```

## Notes

- All scripts use generators to efficiently process large datasets.
- No SQL aggregate functions (e.g., `AVG`) are used for aggregation tasks.
- The code is designed to minimize memory usage by yielding records one at a time.
