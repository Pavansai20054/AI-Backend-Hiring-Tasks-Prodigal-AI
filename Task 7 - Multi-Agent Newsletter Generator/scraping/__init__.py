from .coindesk import scrape_coindesk
from .cointelegraph import scrape_cointelegraph
from .decrypt import scrape_decrypt
from .bankless import scrape_bankless

SCRAPER_FUNCS = [
    scrape_coindesk,
    scrape_cointelegraph,
    scrape_decrypt,
    scrape_bankless,
]