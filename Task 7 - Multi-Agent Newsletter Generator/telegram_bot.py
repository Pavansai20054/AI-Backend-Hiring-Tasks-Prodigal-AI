import os
from telegram import Bot
from telegram.constants import ParseMode
import asyncio
from dotenv import load_dotenv
from config import config
from colorama import Fore, Style

load_dotenv('.env.local')

def split_message(text: str, max_length: int = 4096) -> list:
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

async def send_newsletter_async(message: str):
    try:
        telegram_token = config['TELEGRAM_BOT_TOKEN']
        group_id = config['TELEGRAM_GROUP_ID']
        
        if not telegram_token or not group_id:
            raise ValueError("Telegram credentials not configured")
            
        bot = Bot(token=telegram_token)
        chunks = split_message(message)
        
        for chunk in chunks:
            await bot.send_message(
                chat_id=group_id,
                text=chunk,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=False
            )
            
    except Exception as e:
        print(f"{Fore.RED}Error sending to Telegram: {e}{Style.RESET_ALL}")
        raise

class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=config['TELEGRAM_BOT_TOKEN'])
    
    async def send_newsletter(self, message: str):
        await send_newsletter_async(message)