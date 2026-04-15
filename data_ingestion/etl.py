import sqlite3
from utils.logger import get_logger

logger = get_logger()

def clean_text(text):
    if not text:
        return None
    if text in ["[deleted]", "[removed]"]:
        return None
    return text.strip()

def insert_post(conn, post):
    sql = """
    INSERT OR IGNORE INTO posts
    (id, subreddit, title, body, author, score, timestamp, url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    conn.execute(sql, (
        post["id"],
        post["subreddit"],
        clean_text(post["title"]),
        clean_text(post["body"]),
        post["author"],
        post["score"],
        post["timestamp"],
        post["url"]
    ))

def insert_comment(conn, comment):
    sql = """
    INSERT OR IGNORE INTO comments
    (id, post_id, parent_id, author, body, score, timestamp, depth)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    conn.execute(sql, (
        comment["id"],
        comment["post_id"],
        comment["parent_id"],
        clean_text(comment["author"]),
        clean_text(comment["body"]),
        comment["score"],
        comment["timestamp"],
        comment["depth"]
    ))

def load_to_db(posts, comments):
    logger.info("=== ETL START ===")

    conn = sqlite3.connect("db/reddit.db")

    for p in posts:
        insert_post(conn, p)

    for c in comments:
        insert_comment(conn, c)

    conn.commit()
    conn.close()

    logger.info("ETL finished writing to DB.")
    logger.info("=== ETL END ===")

def get_existing_post_ids():
    conn = sqlite3.connect("db/reddit.db")
    cur = conn.cursor()
    cur.execute("SELECT id FROM posts")
    rows = cur.fetchall()
    conn.close()
    return set(r[0] for r in rows)

def get_existing_comment_ids():
    conn = sqlite3.connect("db/reddit.db")
    cur = conn.cursor()
    cur.execute("SELECT id FROM comments")
    rows = cur.fetchall()
    conn.close()
    return set(r[0] for r in rows)
