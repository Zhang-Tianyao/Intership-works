from reddit_crawler import run_crawler
from etl import load_to_db
from utils.logger import get_logger

logger = get_logger()

def main():
    logger.info("Pipeline start.")

    posts, comments = run_crawler()
    logger.info("Crawler finished.")
    logger.info(f"Got {len(posts)} posts and {len(comments)} comments.")

    load_to_db(posts, comments)

    logger.info("Pipeline done.")

if __name__ == "__main__":
    main()
