"""
3. Retry on Failure Decorator
This module provides a retry_on_failure decorator that retries a function if it raises an exception,
with configurable number of retries and delay between attempts.
"""

import time
import functools

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries the decorated function up to 'retries' times with 'delay' seconds between attempts
    if an exception is raised. If all attempts fail, the last exception is raised.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < retries:
                        print(f"Attempt {attempt} failed: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"Attempt {attempt} failed: {e}. No more retries left.")
            raise last_exception
        return wrapper
    return decorator

# Example usage:
if __name__ == "__main__":
    counter = {"failures": 0}

    @retry_on_failure(retries=4, delay=1)
    def flaky_operation():
        if counter["failures"] < 2:
            counter["failures"] += 1
            raise RuntimeError("Simulated transient error")
        return "Success after retries!"

    print(flaky_operation())
