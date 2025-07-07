import os
from telegram import Bot
from telegram.constants import ParseMode
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv('.env.local')

def split_message(text, max_length=4096):
    paragraphs = text.split('\n\n')
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 2 > max_length:
            chunks.append(current)
            current = para
        else:
            if current:
                current += "\n\n" + para
            else:
                current = para
    if current:
        chunks.append(current)
    return chunks

async def send_newsletter_async(message):
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")  # Your bot token from .env.local
    group_id = os.getenv("TELEGRAM_GROUP_ID")         # Your group/chat id from .env.local
    if telegram_token is None:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not found in environment variables!")
    if group_id is None:
        raise RuntimeError("TELEGRAM_GROUP_ID not found in environment variables!")
    bot = Bot(token=telegram_token)
    chunks = split_message(message)
    for chunk in chunks:
        await bot.send_message(
            chat_id=group_id,
            text=chunk,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=False
        )

def send_newsletter(message):
    asyncio.run(send_newsletter_async(message))