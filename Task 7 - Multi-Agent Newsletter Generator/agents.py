from langchain_core.tools import Tool
from typing import List, Dict
from models import Article
from scraping import SCRAPER_FUNCS
from deduplicate import deduplicate_articles
import warnings
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)
warnings.filterwarnings("ignore", category=UserWarning)

class NewsletterAgents:
    def __init__(self, llm):
        self.llm = llm
        self.tools = self._setup_tools()
        
    def _setup_tools(self):
        def fetch_articles(day_offset: int, articles_per_day: int) -> List[Dict]:
            print(f"{Fore.YELLOW}[Agent]{Style.RESET_ALL} Fetching articles from all sources...")
            articles = []
            for func in SCRAPER_FUNCS:
                try:
                    print(f"{Fore.BLUE}[Agent]{Style.RESET_ALL} Running scraper: {func.__name__}")
                    arts = func(day_offset=day_offset, articles_per_day=articles_per_day)
                    articles.extend(arts)
                    print(f"{Fore.GREEN}[Agent]{Style.RESET_ALL} {len(arts)} articles fetched from {func.__name__}.")
                except Exception as e:
                    print(f"{Fore.RED}[Agent Error]{Style.RESET_ALL} Error in {func.__name__}: {e}")
            print(f"{Fore.YELLOW}[Agent]{Style.RESET_ALL} Total articles fetched: {len(articles)}")
            return articles

        def deduplicate(articles: List[Dict]) -> List[Dict]:
            print(f"{Fore.YELLOW}[Agent]{Style.RESET_ALL} Deduplicating articles...")
            result = deduplicate_articles(articles)
            print(f"{Fore.YELLOW}[Agent]{Style.RESET_ALL} {len(result)} articles remaining after deduplication.")
            return result

        return [
            Tool(
                name="fetch_articles",
                func=fetch_articles,
                description="Fetches articles from configured news sources"
            ),
            Tool(
                name="deduplicate_articles",
                func=deduplicate,
                description="Removes duplicate or similar articles"
            )
        ]

    def run_pipeline(self, day_offset: int, articles_per_day: int) -> List[Article]:
        print(f"{Fore.GREEN}[Pipeline]{Style.RESET_ALL} Starting newsletter agent pipeline...")
        articles = self.tools[0].func(day_offset=day_offset, articles_per_day=articles_per_day)
        deduped_articles = self.tools[1].func(articles=articles)
        print(f"{Fore.GREEN}[Pipeline]{Style.RESET_ALL} Pipeline finished. {len(deduped_articles)} articles ready for summarization.")
        return deduped_articles