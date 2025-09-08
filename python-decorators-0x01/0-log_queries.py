#!/usr/bin/env python3
import sqlite3
import functools

# decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)  # preserves function metadata
    def wrapper(*args, **kwargs):
        # extract query if passed as argument or keyword
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        if query:
            print(f"Executing SQL Query: {query}")
        else:
            print("No SQL Query provided")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
