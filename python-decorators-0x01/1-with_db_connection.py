#!/usr/bin/env python3
import sqlite3
import functools

# decorator to handle DB connection automatically
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # open connection
        conn = sqlite3.connect("users.db")
        try:
            # pass connection as first argument to function
            result = func(conn, *args, **kwargs)
        finally:
            # close connection after function execution
            conn.close()
        return result
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Fetch user by ID with automatic connection handling
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)
