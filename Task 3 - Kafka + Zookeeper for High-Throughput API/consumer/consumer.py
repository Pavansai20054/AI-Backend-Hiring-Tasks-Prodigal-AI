import os
from kafka import KafkaConsumer
import json
import time
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env.local'))

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "events")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:29092")
GROUP_ID = os.getenv("KAFKA_CONSUMER_GROUP", "consumer-group-1")
LOG_FILE = os.getenv("CONSUMER_LOG_FILE", "logs/consumer.log")
DLQ_FILE = os.getenv("DLQ_FILE", "logs/dlq.log")
MAX_RETRIES = 3
RETRY_DELAY = 0.2  # seconds

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

def process_event(event):
    # Simulate random failure (for demo)
    if event.get("fail_me"):
        raise Exception("Random processing error")
    # Simulate processing
    time.sleep(0.001)
    logging.info(f"Processed: {event}")
    print(f"Processed: {event}")  # Print to terminal

def handle_with_retry(event):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            process_event(event)
            return True
        except Exception as e:
            if attempt < MAX_RETRIES:
                print(f"Retry {attempt} for event: {event} due to: {e}")
                time.sleep(RETRY_DELAY)
            else:
                # Log to DLQ
                with open(DLQ_FILE, "a") as f:
                    f.write(json.dumps({"event": event, "error": str(e)}) + "\n")
                logging.error(f"Failed after retries: {event} | Error: {e}")
                print(f"Failed after retries: {event} | Error: {e}")
                return False

def main():
    print(f"Consumer started. Listening to topic '{KAFKA_TOPIC}' at {KAFKA_BROKER}. Press Ctrl+C to stop.")
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=GROUP_ID,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    try:
        for message in consumer:
            event = message.value
            handle_with_retry(event)
    except KeyboardInterrupt:
        print("\nConsumer interrupted by user. Exiting...")

if __name__ == "__main__":
    main()