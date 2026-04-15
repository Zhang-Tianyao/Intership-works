from fetcher import fetch_url
from bs4 import BeautifulSoup
import json
from fetcher import fetch_url
import time
import random
from etl import get_existing_post_ids
from etl import get_existing_comment_ids

from config import load_config
config = load_config()


MAX_COMMENTS_PER_POST = 200


def parse_posts(html, subreddit):
    soup = BeautifulSoup(html, "html.parser")
    posts = []

    for thing in soup.find_all("div", class_="thing"):
        post_id = thing.get("data-fullname")
        if not post_id:
            continue

        title_tag = thing.find("a", class_="title")
        if not title_tag:
            continue

        url = title_tag["href"]
        title = title_tag.text.strip()

        posts.append({
            "id": post_id,
            "subreddit": subreddit,
            "title": title,
            "body": None,
            "author": thing.get("data-author"),
            "score": None,
            "timestamp": None,
            "url": url
        })

    next_button = soup.find("span", class_="next-button")
    next_page = None
    if next_button:
        next_page = next_button.find("a")["href"]

    return posts, next_page



def run_crawler(max_pages=3):
    
    subreddit = config["subreddit"]
    max_pages = config["crawler"]["max_pages"]
    enable_comments = config["crawler"]["enable_comments"]
    enable_incremental = config["crawler"]["enable_incremental"]
    max_comments_per_post = config["crawler"]["max_comments_per_post"]
    
    existing_posts = get_existing_post_ids()
    
    url = f"https://old.reddit.com/r/{subreddit}/hot/"

    all_posts = []
    all_comments = []

    for _ in range(max_pages):
        html = fetch_url(url)
        posts, next_page = parse_posts(html, subreddit)

        all_posts.extend(posts)

        for p in posts:
            if not enable_comments:
                continue

            if p["id"] in existing_posts:
                print(f"Skip existing post {p['id']}")
                continue

            fullname = p["id"]
            post_id = fullname[3:]

            try:
                time.sleep(random.uniform(2.0, 4.0))
                raw_comments = fetch_comments(post_id)
                comments = parse_comment_tree(raw_comments, fullname)
                all_comments.extend(comments)
            except Exception as e:
                print(f"Failed to fetch comments for {fullname}: {e}")

        if not next_page:
            break

        url = next_page

    return all_posts, all_comments




def fetch_comments(post_id):
    url = f"https://old.reddit.com/comments/{post_id}.json"
    html = fetch_url(url)
    data = json.loads(html)

    return data[1]["data"]["children"]

def parse_comment_tree(children, post_id, depth=0):
    
    max_comments_per_post = config["crawler"]["max_comments_per_post"]
    
    existing_comments = get_existing_comment_ids()  # 获取已存在的评论ID集合
    
    comments = []

    for child in children:
        if len(comments) >= max_comments_per_post:
            break

        kind = child.get("kind")
        data = child.get("data", {})

        if kind == "more":
            continue

        comment_id = data.get("id")
        if not comment_id:
            continue

        comments.append({
            "id": comment_id,
            "post_id": post_id,
            "parent_id": data.get("parent_id"),
            "author": data.get("author"),
            "body": data.get("body"),
            "score": data.get("score"),
            "timestamp": data.get("created_utc"),
            "depth": depth
        })

        if data.get("replies"):
            replies = data["replies"]["data"]["children"]
            comments.extend(parse_comment_tree(replies, post_id, depth + 1))
            
        if len(comments) >= MAX_COMMENTS_PER_POST:
            break

        comments = [c for c in comments if c["id"] not in existing_comments]


    return comments

