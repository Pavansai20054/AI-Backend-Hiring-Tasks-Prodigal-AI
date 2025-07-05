import asyncio
import websockets
import json
import os
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import asyncpg
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv(dotenv_path=".env.local")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

BINANCE_WS_URL = os.getenv("BINANCE_WS_URL", "wss://stream.binance.com:9443/stream?streams=btcusdt@trade/ethusdt@trade")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS price_ticks (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    price_str TEXT NOT NULL,
    price NUMERIC(30, 12) NOT NULL,
    ts TIMESTAMPTZ NOT NULL
);
"""

INSERT_TICK_SQL = """
INSERT INTO price_ticks (symbol, price_str, price, ts)
VALUES ($1, $2, $3, $4);
"""

async def get_postgres_pool():
    pool = await asyncpg.create_pool(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB,
        min_size=1,
        max_size=5,
        timeout=5,
    )
    async with pool.acquire() as conn:
        await conn.execute(CREATE_TABLE_SQL)
    return pool

async def write_tick(pool, symbol, price_str, ts):
    try:
        price_decimal = Decimal(price_str)
        dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
    except (InvalidOperation, ValueError):
        print(f"[Warning] Invalid price: {price_str}")
        return

    async with pool.acquire() as conn:
        await conn.execute(INSERT_TICK_SQL, symbol, str(price_decimal), price_decimal, dt)
    print(f"[{symbol}] {price_decimal} at {dt.strftime('%Y-%m-%d %H:%M:%S.%f UTC')}")

async def stream_binance():
    pool = await get_postgres_pool()
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
                            await write_tick(pool, symbol, price, ts)
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
        print("\nStopped Binance WebSocket to PostgreSQL streamer.")