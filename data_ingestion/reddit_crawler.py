# reddit_crawler.py

def run_crawler():
    # 用硬编码数据模拟爬虫结果
    posts = [
        {
            "id": "t3_abc123",
            "subreddit": "steam",
            "title": "Why does Steam crash?",
            "body": "Steam keeps crashing on startup.",
            "author": "user1",
            "score": 152,
            "timestamp": 1710000000,  # Unix 时间戳
            "url": "https://www.reddit.com/r/steam/comments/abc123/"
        }
    ]

    comments = [
        {
            "id": "t1_cmt001",
            "post_id": "t3_abc123",
            "parent_id": "t3_abc123",
            "author": "user2",
            "body": "I have the same issue.",
            "score": 20,
            "timestamp": 1710000300,
            "depth": 0
        }
    ]

    return posts, comments
