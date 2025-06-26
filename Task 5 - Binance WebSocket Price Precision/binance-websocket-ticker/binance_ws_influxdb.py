import asyncio
import websockets
import json
from datetime import datetime, timezone
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from decimal import Decimal, InvalidOperation
from dotenv import load_dotenv
import os

# Load environment variables from .env.local file
load_dotenv(dotenv_path=".env.local")

# InfluxDB connection settings
INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")
BINANCE_WS_URL = os.getenv("BINANCE_WS_URL")

def get_influxdb_client():
    client = InfluxDBClient(
        url=INFLUXDB_URL,
        token=INFLUXDB_TOKEN,
        org=INFLUXDB_ORG,
        timeout=5000
    )
    return client

async def write_tick(write_api, symbol, price_str, ts):
    dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
    try:
        price_decimal = Decimal(price_str)
        price_float = float(price_decimal)
    except (InvalidOperation, ValueError):
        print(f"[Warning] Invalid price: {price_str}")
        return

    point = (
        Point("price_ticks")
        .tag("symbol", symbol)
        .field("price", price_float)
        .field("price_str", str(price_decimal))
        .time(dt, WritePrecision.MS)
    )
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
    print(f"[{symbol}] {price_decimal} at {dt.strftime('%Y-%m-%d %H:%M:%S.%f UTC')}")

async def stream_binance():
    client = get_influxdb_client()
    write_api = client.write_api(write_options=SYNCHRONOUS)

    while True:
        try:
            print("Connecting to Binance WebSocket...")
            async with websockets.connect(
                BINANCE_WS_URL,
                ping_interval=15,
                ping_timeout=10,
                close_timeout=5,
                max_queue=512,
            ) as ws:
                print("✅ Connected! Streaming BTCUSDT & ETHUSDT ticks...\nPress Ctrl+C to stop.")
                async for message in ws:
                    try:
                        data = json.loads(message)
                        payload = data.get("data")
                        if payload and "s" in payload and "p" in payload and "T" in payload:
                            symbol = payload["s"]
                            price = payload["p"]
                            ts = payload["T"]
                            await write_tick(write_api, symbol, price, ts)
                    except Exception as ex:
                        print(f"[Warning] Failed to process message: {ex}")
        except (websockets.ConnectionClosed, websockets.InvalidStatusCode, asyncio.TimeoutError) as e:
            print(f"[Error] WebSocket disconnected or error: {e}")
            print("Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"[Error] Non-WebSocket error: {e}")
            print("Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(stream_binance())
    except KeyboardInterrupt:
        print("\nStopped Binance WebSocket to InfluxDB streamer.")