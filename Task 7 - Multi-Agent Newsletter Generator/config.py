import os
from dotenv import load_dotenv
from typing import List, Optional
import argparse

load_dotenv('.env.local')

# Configuration with CLI overrides
def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--publications', nargs='+', default=None, 
                       help='List of publications to scrape')
    parser.add_argument('--top-n', type=int, default=None,
                       help='Number of top articles to select')
    parser.add_argument('--simulation-days', type=int, default=None,
                       help='Number of days to simulate')
    args = parser.parse_args()

    return {
        'GEMINI_API_KEY': os.getenv("GEMINI_API_KEY"),
        'TELEGRAM_BOT_TOKEN': os.getenv("TELEGRAM_BOT_TOKEN"),
        'TELEGRAM_GROUP_ID': os.getenv("TELEGRAM_GROUP_ID"),
        'PUBLICATIONS': args.publications or [
            "coindesk",
            "cointelegraph",
            "decrypt",
            "bankless",
        ],
        'TOP_N_ARTICLES': args.top_n or int(os.getenv("TOP_N_ARTICLES", 10)),
        'SIMULATION_DAYS': args.simulation_days or int(os.getenv("SIMULATION_DAYS", 2)),
        'CHROMA_PERSIST_DIR': os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"),
    }

config = get_config()