import os
from dotenv import load_dotenv

load_dotenv('.env.local')

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")

PUBLICATIONS = [
    "coindesk",
    "cointelegraph",
    "decrypt",
    "bankless",
]

SIMULATION_DAYS = 2
TOP_N_ARTICLES = 10