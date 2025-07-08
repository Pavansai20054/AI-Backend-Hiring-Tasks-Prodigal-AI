import os
from datetime import datetime, timedelta
from colorama import init, Fore, Back, Style
from typing import Optional
import asyncio
from config import config
from agents import NewsletterAgents
from chroma_manager import ChromaManager
from summarizer import summarize_articles
from newsletter import compose_newsletter
from telegram_bot import TelegramBot

init(autoreset=True)

# Define colorful symbols and styles
SYM_INFO = f"{Fore.CYAN}ℹ{Style.RESET_ALL}"
SYM_SUCCESS = f"{Fore.GREEN}✓{Style.RESET_ALL}"
SYM_WARNING = f"{Fore.YELLOW}⚠{Style.RESET_ALL}"
SYM_ERROR = f"{Fore.RED}✗{Style.RESET_ALL}"
SYM_AGENT = f"{Fore.MAGENTA}⚙{Style.RESET_ALL}"

def print_header(text):
    print(f"\n{Fore.BLUE}╒{'═'*(len(text)+2)}╕")
    print(f"│ {Fore.CYAN}{text.upper()}{Fore.BLUE} │")
    print(f"╘{'═'*(len(text)+2)}╛{Style.RESET_ALL}")

def print_agent_status(agent_name, status, message):
    colors = {
        'start': Fore.BLUE,
        'working': Fore.YELLOW,
        'success': Fore.GREEN,
        'error': Fore.RED
    }
    print(f"{SYM_AGENT} {colors.get(status, Fore.WHITE)}{agent_name}: {message}{Style.RESET_ALL}")

async def run_newsletter_day(day_str: str, day_offset: int = 0, top_n: int = 10) -> Optional[str]:
    try:
        print_header(f"processing day {day_str}")
        
        # Initialize LLM
        print_agent_status("LLM Agent", "start", "Initializing Ollama...")
        from langchain_ollama import OllamaLLM
        llm = OllamaLLM(model="llama3:8b")
        print_agent_status("LLM Agent", "success", "Ready to generate summaries")
        
        # Initialize agents
        print_agent_status("News Agents", "start", "Initializing pipeline...")
        agents = NewsletterAgents(llm)
        
        # Run agent pipeline
        print_agent_status("Scraper Agent", "working", "Fetching articles...")
        articles = agents.run_pipeline(day_offset, top_n*2)
        print_agent_status("Scraper Agent", "success", f"Found {len(articles)} articles")
        
        # Store in ChromaDB
        if hasattr(chroma, 'available') and chroma.available:
            print_agent_status("VectorDB Agent", "working", "Storing articles...")
            chroma.add_articles(articles)
            print_agent_status("VectorDB Agent", "success", "Articles stored")
        
        # Summarize articles
        print_agent_status("Summarizer Agent", "working", "Generating summaries...")
        summaries = summarize_articles(articles[:top_n])
        print_agent_status("Summarizer Agent", "success", f"Generated {len(summaries)} summaries")
        
        # Compose newsletter
        print_agent_status("Composer Agent", "working", "Formatting newsletter...")
        newsletter = compose_newsletter(day_str, summaries)
        print_agent_status("Composer Agent", "success", "Newsletter composed")
        
        # Send to Telegram
        if "test" not in day_str.lower():
            print_agent_status("Telegram Agent", "working", "Sending newsletter...")
            await telegram_bot.send_newsletter(newsletter)  # Fixed: removed _async suffix
            print_agent_status("Telegram Agent", "success", "Newsletter sent")
        
        return newsletter
        
    except Exception as e:
        print_agent_status("System", "error", f"Pipeline error: {e}")
        return None

def simulate_days(n_days: int = 2):
    now = datetime.now()
    for i in range(n_days):
        day = now + timedelta(days=i)
        asyncio.run(run_newsletter_day(
            day_str=day.strftime("%Y-%m-%d"), 
            day_offset=i, 
            top_n=config['TOP_N_ARTICLES']
        ))

if __name__ == "__main__":
    try:
        print_header("web3 newsletter generator")
        print(f"{SYM_INFO} {Fore.CYAN}Initializing components...{Style.RESET_ALL}")
        
        chroma = ChromaManager()
        telegram_bot = TelegramBot()
        
        print(f"{SYM_INFO} {Fore.CYAN}Sources: {', '.join(config['PUBLICATIONS'])}{Style.RESET_ALL}")
        print(f"{SYM_INFO} {Fore.CYAN}Top articles per day: {config['TOP_N_ARTICLES']}{Style.RESET_ALL}")
        
        if config['SIMULATION_DAYS'] > 0:
            print(f"{SYM_INFO} {Fore.CYAN}Simulating {config['SIMULATION_DAYS']} days{Style.RESET_ALL}")
            simulate_days(config['SIMULATION_DAYS'])
        else:
            print(f"{SYM_INFO} {Fore.CYAN}Running for current day{Style.RESET_ALL}")
            asyncio.run(run_newsletter_day(
                day_str=datetime.now().strftime("%Y-%m-%d"),
                day_offset=0,
                top_n=config['TOP_N_ARTICLES']
            ))
        
        print(f"\n{SYM_SUCCESS} {Fore.GREEN}All tasks completed successfully!{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"\n{SYM_ERROR} {Fore.RED}Fatal error: {e}{Style.RESET_ALL}")