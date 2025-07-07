import feedparser
import requests

def scrape_bankless(day_offset=0, articles_per_day=10):
    url = "https://www.bankless.com/feed"
    resp = requests.get(url, timeout=10)
    feed = feedparser.parse(resp.content)
    entries = feed.entries
    start = day_offset * articles_per_day
    end = start + articles_per_day
    for entry in entries[start:end]:
        yield {
            "title": entry.title,
            "url": entry.link,
            "source": "Bankless"
        }

if __name__ == "__main__":
    for offset in range(2):  # day_offset=0 and day_offset=1
        print(f"\n=== day_offset={offset} ===")
        for art in scrape_bankless(day_offset=offset):
            print(art)