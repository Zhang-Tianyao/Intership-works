import sqlite3

conn = sqlite3.connect("db/reddit.db")
cur = conn.cursor()

cur.execute("DELETE FROM posts;")
cur.execute("DELETE FROM comments;")

conn.commit()
conn.close()

print("Database cleared.")
