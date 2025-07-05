from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Kubernetes HPA!"}

@app.get("/load")
def load_cpu(duration: int = 10):
    """
    Loads CPU for `duration` seconds. Default: 10 seconds.
    """
    end = time.time() + duration
    while time.time() < end:
        _ = 12345 * 67890  # Busy loop to load CPU
    return {"message": f"Loaded CPU for {duration} seconds"}