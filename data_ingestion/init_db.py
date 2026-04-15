import sqlite3
import os

def init_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect("db/reddit.db")

    with open("db/schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    init_db()
