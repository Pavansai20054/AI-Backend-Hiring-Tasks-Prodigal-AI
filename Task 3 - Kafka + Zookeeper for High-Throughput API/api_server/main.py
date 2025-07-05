import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kafka import KafkaProducer
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env.local'))

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "events")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:29092")

app = FastAPI(title="Kafka High-Throughput API Example")

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    linger_ms=5
)

class Event(BaseModel):
    user_id: int
    event_type: str
    data: dict

@app.post("/register_event")
async def register_event(event: Event):
    try:
        producer.send(KAFKA_TOPIC, event.dict())
        producer.flush()
        return {"status": "queued", "event": event.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_status")
async def get_status():
    # This is a dummy endpoint. For real stats, you need a DB or metric store.
    return {
        "message": "Status endpoint is a stub. Implement with DB/metrics for real usage."
    }