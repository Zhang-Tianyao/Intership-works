import sqlite3

conn = sqlite3.connect("db/reddit.db")
cur = conn.cursor()

print("Posts:")
cur.execute("SELECT * FROM posts;")
print(cur.fetchall())

print("\nComments:")
cur.execute("SELECT * FROM comments;")
print(cur.fetchall())

conn.close()
