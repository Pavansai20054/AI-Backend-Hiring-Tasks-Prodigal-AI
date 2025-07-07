import requests
from bs4 import BeautifulSoup
import time

def scrape_cointelegraph(day_offset=0, articles_per_day=10, max_retries=3):
    url = "https://cointelegraph.com/rss"
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, timeout=20)
            soup = BeautifulSoup(resp.content, "xml")
            articles = []
            items = soup.find_all("item")
            start = day_offset * articles_per_day
            end = start + articles_per_day
            for item in items[start:end]:
                title = item.title.text.strip()
                link = item.link.text.strip()
                articles.append({
                    "title": title,
                    "url": link,
                    "source": "CoinTelegraph"
                })
            return articles
        except Exception as e:
            print(f"Attempt {attempt+1} failed for CoinTelegraph: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise

if __name__ == "__main__":
    for offset in range(2):  # day_offset=0 and day_offset=1
        print(f"\n=== day_offset={offset} ===")
        for art in scrape_cointelegraph(day_offset=offset):
            print(art)