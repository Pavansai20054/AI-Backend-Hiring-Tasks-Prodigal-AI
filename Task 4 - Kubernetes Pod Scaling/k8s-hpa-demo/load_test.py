import requests
import threading

URL = "http://127.0.0.1:7000/load?duration=10"
def hit_load():
    for _ in range(20):
        try:
            r = requests.get(URL)
            print(r.json())
        except Exception as e:
            print(e)

threads = [threading.Thread(target=hit_load) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()