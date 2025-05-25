"""
3. Concurrent Database Queries with aiosqlite and asyncio.gather
This script demonstrates running multiple database queries concurrently using aiosqlite and asyncio.
"""

import asyncio
import aiosqlite

DB_PATH = ":memory:"

async def setup_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        await db.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [("Alice", 30), ("Bob", 45), ("Carol", 50), ("Dave", 25)]
        )
        await db.commit()

async def async_fetch_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            users = await cursor.fetchall()
            return users

async def fetch_concurrently():
    await setup_db()
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:", all_users)
    print("Users older than 40:", older_users)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
