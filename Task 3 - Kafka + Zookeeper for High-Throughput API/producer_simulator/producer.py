import asyncio
import aiohttp
import random
import time
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env.local'))

API_URL = "http://localhost:8000/register_event"
TOTAL_REQUESTS = 10000
CONCURRENT_REQUESTS = 100

async def send_event(session, idx):
    payload = {
        "user_id": random.randint(1, 1000),
        "event_type": random.choice(["click", "view", "purchase"]),
        "data": {"value": random.random(), "idx": idx}
    }
    try:
        async with session.post(API_URL, json=payload, timeout=5) as resp:
            result = await resp.json()
            return {"result": result, "idx": idx}
    except Exception as e:
        return {"error": str(e), "idx": idx}

async def main():
    print(f"Producer started. Sending events to {API_URL}")
    start = time.perf_counter()
    sent = 0
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(TOTAL_REQUESTS):
                tasks.append(send_event(session, i))
                if len(tasks) >= CONCURRENT_REQUESTS:
                    results = await asyncio.gather(*tasks)
                    sent += len(results)
                    if sent % 1000 == 0 or sent == TOTAL_REQUESTS:
                        print(f"Sent {sent} events...")
                    for r in results:
                        if "error" in r:
                            print(f"Error at idx {r['idx']}: {r['error']}")
                    tasks = []
            if tasks:
                results = await asyncio.gather(*tasks)
                sent += len(results)
                for r in results:
                    if "error" in r:
                        print(f"Error at idx {r['idx']}: {r['error']}")
        print(f"Sent {TOTAL_REQUESTS} events in {time.perf_counter() - start:.2f} sec.")
    except KeyboardInterrupt:
        print("\nProducer interrupted by user. Exiting...")

if __name__ == "__main__":
    asyncio.run(main())