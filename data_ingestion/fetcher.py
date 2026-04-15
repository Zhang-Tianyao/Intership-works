import random
import time
import requests
from config import load_config

config = load_config()
UA_LIST = config["user_agents"]

session = requests.Session()

def fetch_url(url, min_delay=None, max_delay=None):
    if min_delay is None:
        min_delay = config["crawler"]["fetch_delay_min"]
    if max_delay is None:
        max_delay = config["crawler"]["fetch_delay_max"]

    time.sleep(random.uniform(min_delay, max_delay))

    headers = {"User-Agent": random.choice(UA_LIST)}

    resp = session.get(url, headers=headers, timeout=10)

    if resp.status_code == 429:
        print("Hit rate limit, sleeping 10 seconds...")
        time.sleep(10)
        return fetch_url(url, min_delay, max_delay)

    resp.raise_for_status()
    return resp.text
