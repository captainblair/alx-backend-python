#!/usr/bin/env python3
"""
Reusable Query Context Manager for executing queries
"""

import sqlite3


class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Open database connection
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Execute the query
        self.cursor.execute(self.query, self.params)

        # Fetch results
        self.results = self.cursor.fetchall()
        return self.results  # Results are returned directly

    def __exit__(self, exc_type, exc_value, traceback):
        # Close cursor and connection safely
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Setup database for demo
    with sqlite3.connect("users.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
        )
        cur.execute("DELETE FROM users")  # clear old rows
        cur.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [("Alice", 30), ("Bob", 22), ("Charlie", 40)],
        )
        conn.commit()

    # Use our context manager
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)

    with ExecuteQuery("users.db", query, param) as results:
        for row in results:
            print(row)
