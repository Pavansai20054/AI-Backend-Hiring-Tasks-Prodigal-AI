import requests
from bs4 import BeautifulSoup

def scrape_decrypt(day_offset=0, articles_per_day=10):
    url = "https://decrypt.co/feed"
    resp = requests.get(url, timeout=10)
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
            "source": "Decrypt"
        })
    return articles

if __name__ == "__main__":
    for offset in range(2):  # day_offset=0 and day_offset=1
        print(f"\n=== day_offset={offset} ===")
        for art in scrape_decrypt(day_offset=offset):
            print(art)