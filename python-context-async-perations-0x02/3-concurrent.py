#!/usr/bin/env python3
"""
Concurrent Asynchronous Database Queries using aiosqlite and asyncio.gather
"""

import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users from the database"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users():
    """Fetch users older than 40 from the database"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    """Run both queries concurrently"""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    all_users, older_users = results

    print("All Users:")
    for row in all_users:
        print(row)

    print("\nUsers older than 40:")
    for row in older_users:
        print(row)


if __name__ == "__main__":
    # Setup demo DB (optional, remove if DB already exists)
    async def setup_db():
        async with aiosqlite.connect("users.db") as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)"
            )
            await db.execute("DELETE FROM users")  # clear old data
            await db.executemany(
                "INSERT INTO users (name, age) VALUES (?, ?)",
                [("Alice", 30), ("Bob", 45), ("Charlie", 50), ("David", 25)],
            )
            await db.commit()

    asyncio.run(setup_db())   # ensure table + sample data exist
    asyncio.run(fetch_concurrently())
