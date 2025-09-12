#!/usr/bin/env python3
"""
Class-based context manager for handling database connections
"""

import sqlite3  # Using sqlite3 for demonstration, but can adapt to MySQL, Postgres, etc.


class DatabaseConnection:
    def __init__(self, db_name):
        # store the database name
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # open connection when entering context
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        # close connection when exiting context
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Example usage of the context manager
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()

        # make sure table exists for demo
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)"
        )
        cursor.execute("INSERT INTO users (name) VALUES (?)", ("Blair",))
        conn.commit()

        # perform the query
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()

        # print results
        for row in results:
            print(row)
