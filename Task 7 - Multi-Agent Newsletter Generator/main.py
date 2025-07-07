import os
from datetime import datetime, timedelta
from colorama import init, Fore, Back, Style
import platform

from scraping import SCRAPER_FUNCS
from config import SIMULATION_DAYS, TOP_N_ARTICLES
from summarizer import summarize_articles
from newsletter import compose_newsletter
from telegram_bot import send_newsletter

# Initialize colorama
init(autoreset=True)

# Define the output directory for markdown files
MARKDOWN_DIR = os.path.join(
    os.path.dirname(__file__),
    "markdown_files"
)
os.makedirs(MARKDOWN_DIR, exist_ok=True)

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Futuristic symbols
SYM_SUCCESS = "◈"  # Diamond
SYM_WARNING = "⌾"  # Square
SYM_ERROR = "⚡"    # Lightning
SYM_INFO = "◌"     # Circle
SYM_PROGRESS = "⇶" # Triple arrow
SYM_HEADER = "≋"   # Waves

def print_header(text):
    print(Fore.CYAN + Style.BRIGHT + SYM_HEADER * 50)
    print(Fore.MAGENTA + Style.BRIGHT + text.center(50))
    print(Fore.CYAN + Style.BRIGHT + SYM_HEADER * 50 + Style.RESET_ALL)

def print_success(text):
    print(Fore.GREEN + Style.BRIGHT + f"{SYM_SUCCESS} {text}" + Style.RESET_ALL)

def print_warning(text):
    print(Fore.YELLOW + Style.BRIGHT + f"{SYM_WARNING} {text}" + Style.RESET_ALL)

def print_error(text):
    print(Fore.RED + Style.BRIGHT + f"{SYM_ERROR} {text}" + Style.RESET_ALL)

def print_info(text):
    print(Fore.BLUE + Style.BRIGHT + f"{SYM_INFO} {text}" + Style.RESET_ALL)

def print_progress(text):
    print(Fore.CYAN + Style.BRIGHT + f"{SYM_PROGRESS} {text}" + Style.RESET_ALL)

def fetch_all_articles(day_offset=0, articles_per_day=10):
    articles = []
    for func in SCRAPER_FUNCS:
        try:
            arts = func(day_offset=day_offset, articles_per_day=articles_per_day)
            if hasattr(arts, '__iter__') and not isinstance(arts, list):
                arts = list(arts)
            articles.extend(arts)
        except Exception as e:
            print_error(f"Error scraping {func.__name__}: {e}")
    
    source_counts = {}
    for a in articles:
        source = a.get("source", "Unknown")
        source_counts[source] = source_counts.get(source, 0) + 1
    print_info(f"Articles per source: {source_counts}")
    return articles

def deduplicate_articles(articles):
    seen = set()
    deduped = []
    for art in articles:
        key = (art.get("title"), art.get("url"))
        if key not in seen:
            deduped.append(art)
            seen.add(key)
    print_success(f"Deduplicated to {len(deduped)} articles.")
    return deduped

def select_top_n_articles(articles, n):
    top_articles = articles[:n]
    print_success(f"Selected top {n} articles.")
    return top_articles

def run_newsletter_day(day_str, day_offset, top_n=10):
    print_header(f"📡 DAY {day_str} | NEWS COLLECTION")
    
    print_progress("Scanning news sources across the web...")
    articles = fetch_all_articles(day_offset=day_offset, articles_per_day=top_n*2)
    print_info(f"Acquired {len(articles)} raw data points")
    
    print_progress("Filtering duplicate transmissions...")
    articles = deduplicate_articles(articles)
    
    print_progress("Isolating priority signals...")
    articles = select_top_n_articles(articles, top_n)

    print_progress("Analyzing content with neural networks...")
    summaries = summarize_articles(articles)
    
    print_progress("Compiling final transmission...")
    newsletter = compose_newsletter(day_str, summaries)

    filename = f"newsletter_{day_str}.md"
    filepath = os.path.join(MARKDOWN_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(newsletter)
    print_success(f"Data archived to {Fore.MAGENTA}{filepath}")

    print_progress("Initiating broadcast sequence...")
    try:
        send_newsletter(newsletter)
        print_success("Transmission successful!")
    except Exception as e:
        print_error(f"Broadcast failure: {e}")

def simulate_days(n_days, top_n=10):
    now = datetime.now()
    for i in range(n_days):
        day = now + timedelta(days=i)
        run_newsletter_day(day_str=day.strftime("%Y-%m-%d"), day_offset=i, top_n=top_n)

if __name__ == "__main__":
    clear_screen()
    print_header("🌌 WEB3 NEWS NETWORK v1.0")
    print(Fore.YELLOW + Style.BRIGHT + "Initializing quantum news aggregation matrix..." + Style.RESET_ALL)
    print(Fore.CYAN + f"System parameters: {SIMULATION_DAYS} cycles, {TOP_N_ARTICLES} priority signals" + Style.RESET_ALL)
    print()
    
    try:
        simulate_days(SIMULATION_DAYS, top_n=TOP_N_ARTICLES)
        print_header("✅ MISSION COMPLETE")
        print(Fore.GREEN + Style.BRIGHT + "All transmissions processed successfully!" + Style.RESET_ALL)
    except Exception as e:
        print_error(f"System critical error: {e}")
        print(Fore.RED + Style.BRIGHT + "Emergency shutdown initiated!" + Style.RESET_ALL)