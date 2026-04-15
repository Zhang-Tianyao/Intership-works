import random
import time
import requests

HEADERS = {
    "User-Agent": random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)"
    ])
}

def fetch_url(url, min_delay=1.0, max_delay=2.5):
    time.sleep(random.uniform(min_delay, max_delay))

    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    return resp.text
