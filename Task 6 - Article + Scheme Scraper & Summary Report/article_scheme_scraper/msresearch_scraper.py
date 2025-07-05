import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime
from colorama import Fore, Style, init
import sys
import os
import json
import re

# Initialize colorama
init(autoreset=True)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_console()
    print(Fore.CYAN + r"""[Microsoft Research Blog Scraper Header]""")
    print(Fore.YELLOW + " Microsoft Research Blog Scraper " + Style.RESET_ALL)
    print(Fore.GREEN + "="*60 + Style.RESET_ALL)
    print(Fore.MAGENTA + " • Scrapes full article content including text and metadata")
    print(Fore.MAGENTA + " • Visits each article page individually for complete data")
    print(Fore.MAGENTA + " • Saves results in CSV and JSON formats")
    print(Fore.GREEN + "="*60 + Style.RESET_ALL)

def create_output_directories():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    outputs_dir = os.path.join(script_dir, "..", "outputs", "microsoft-articles")
    csv_dir = os.path.join(outputs_dir, "csv-files")
    json_dir = os.path.join(outputs_dir, "json-files")
    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)
    csv_display_path = os.path.join("outputs", "microsoft-articles", "csv-files")
    json_display_path = os.path.join("outputs", "microsoft-articles", "json-files")
    print(Fore.CYAN + "✔ Output directories created/verified:" + Style.RESET_ALL)
    print(Fore.WHITE + "   • CSV: " + Fore.GREEN + f"{csv_display_path}" + Style.RESET_ALL)
    print(Fore.WHITE + "   • JSON: " + Fore.GREEN + f"{json_display_path}" + Style.RESET_ALL)
    return csv_dir, json_dir

async def show_progress(current, total):
    bar_length = 30
    progress = float(current)/float(total)
    block = int(round(bar_length * progress))
    percent = round(progress * 100, 2)
    progress_bar = (Fore.GREEN + "█" * block + 
                   Fore.YELLOW + "░" * (bar_length - block) + 
                   Style.RESET_ALL)
    sys.stdout.write(f"\r[{progress_bar}] {percent}% ({current}/{total} articles)")
    sys.stdout.flush()

def clean_url(url):
    """Standardize and clean URLs to ensure they're always in a valid format."""
    if not url or url == "No link":
        return url
    url = url.replace('\\/', '/')
    url = url.strip()
    # If it's a relative MS blog link, prepend the full base
    if url.startswith('/en-us/research/blog/'):
        return f"https://www.microsoft.com{url}"
    # If it starts with just /research/blog/, also prepend
    if url.startswith('/research/blog/'):
        return f"https://www.microsoft.com/en-us{url}"
    # If it's a partial path with no leading slash, prepend full
    if not url.startswith('http'):
        if url.startswith('research/blog/'):
            return f"https://www.microsoft.com/en-us/{url}"
        elif not url.startswith('/'):
            return f"https://www.microsoft.com/en-us/research/blog/{url}"
    # If it's already absolute, return as is
    return url

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text

async def scroll_full_page(page):
    last_height = await page.evaluate("() => document.body.scrollHeight")
    while True:
        await page.mouse.wheel(0, 700)
        await asyncio.sleep(0.25)
        new_height = await page.evaluate("() => document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

async def scrape_article_page(context, article_url):
    article_data = {
        "title": "",
        "link": article_url,
        "author": "",
        "date": "",
        "categories": [],
        "content": "",
        "full_text": ""
    }
    try:
        page = await context.new_page()
        await page.goto(article_url, timeout=40000)
        await page.wait_for_selector('body', timeout=10000)
        await scroll_full_page(page)

        # Title
        title = await page.query_selector('h1')
        if title:
            article_data["title"] = clean_text(await title.inner_text())

        # Author
        authors = []
        author_section = await page.query_selector('div:has-text("By ")')
        if author_section:
            author_text = await author_section.inner_text()
            authors_found = re.findall(r'By\s+([^,]+)', author_text)
            if authors_found:
                authors.extend(authors_found)
        byline_links = await page.query_selector_all('a[href*="/en-us/research/people/"]')
        for byline in byline_links:
            atext = clean_text(await byline.inner_text())
            if atext and atext not in authors:
                authors.append(atext)
        article_data["author"] = ", ".join(authors).strip()

        # Date
        date_node = await page.query_selector('time')
        if date_node:
            article_data["date"] = clean_text(await date_node.inner_text())
        else:
            published = await page.query_selector('div:has-text("Published")')
            if published:
                pub_text = await published.inner_text()
                date_match = re.search(r'Published\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})', pub_text)
                if date_match:
                    article_data["date"] = date_match.group(1)

        # Categories
        cats = []
        cat_nodes = await page.query_selector_all('aside [aria-label="Research Areas"] a, aside .tag-list a, aside .topics-list a')
        for cat in cat_nodes:
            text = await cat.inner_text()
            if text:
                cats.append(clean_text(text))
        article_data["categories"] = cats

        # Main content
        content_blocks = []
        main_section = await page.query_selector('main')
        if not main_section:
            main_section = await page.query_selector('article')
        if not main_section:
            main_section = await page.query_selector('div[role="main"]')
        if main_section:
            # Try to extract all visible text blocks, links, and section headers
            nodes = await main_section.query_selector_all('h1,h2,h3,h4,h5,p,li,blockquote,a')
            for node in nodes:
                t = await node.inner_text()
                t = clean_text(t)
                if t and t not in content_blocks:
                    content_blocks.append(t)
        article_data["content"] = "\n".join(content_blocks)

        # Full text
        article_data["full_text"] = "\n".join(filter(None, [
            article_data["title"],
            f"Author: {article_data['author']}",
            f"Date: {article_data['date']}",
            f"Categories: {', '.join(article_data['categories'])}",
            article_data["content"]
        ]))

        await page.close()
    except Exception as e:
        print(Fore.YELLOW + f"⚠ Error scraping article page {article_url}: {str(e)}" + Style.RESET_ALL)
    return article_data

async def scrape_msresearch():
    print_header()
    csv_dir, json_dir = create_output_directories()
    while True:
        try:
            num_articles = int(input(Fore.BLUE + "\n🔢 How many articles would you like to scrape? (Enter positive Integer): " + Style.RESET_ALL))
            if num_articles > 0:
                print(Fore.GREEN + f"✅ Great! I'll fetch {num_articles} articles for you!" + Style.RESET_ALL)
                break
            print(Fore.RED + "❌ Please enter a positive number." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "❌ Invalid input. Please enter a number." + Style.RESET_ALL)

    print(Fore.CYAN + "\n🚀 Starting scrape..." + Style.RESET_ALL)
    start_time = datetime.now()
    data = []

    async with async_playwright() as p:
        print(Fore.BLUE + "\n🖥️  Launching browser... (this may take a moment)" + Style.RESET_ALL)
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        context = await browser.new_context()
        page = await context.new_page()

        print(Fore.BLUE + "\n🌐 Navigating to Microsoft Research Blog..." + Style.RESET_ALL)
        try:
            await page.goto("https://www.microsoft.com/en-us/research/blog/", timeout=30000)
            print(Fore.GREEN + "✔ Successfully loaded the blog page" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"✖ Failed to load page: {str(e)}" + Style.RESET_ALL)
            await browser.close()
            return

        print(Fore.CYAN + "\n🔍 Scraping articles..." + Style.RESET_ALL)
        page_num = 1
        consecutive_failed_pages = 0

        while len(data) < num_articles and consecutive_failed_pages < 3:
            try:
                await page.wait_for_selector('article', timeout=10000)
                articles = await page.query_selector_all('article')
                print(Fore.BLUE + f"\n📄 Processing page {page_num} ({len(articles)} articles found)..." + Style.RESET_ALL)
                for i, article in enumerate(articles):
                    if len(data) >= num_articles:
                        break
                    try:
                        await article.scroll_into_view_if_needed()
                        await asyncio.sleep(0.2)
                        # Get article link
                        link_elem = await article.query_selector('a[href*="/research/blog/"]')
                        link = None
                        if link_elem:
                            href = await link_elem.get_attribute('href')
                            if href:
                                link = clean_url(href)
                        if not link:
                            continue
                        # Scrape in new tab for stability and to allow scrolling
                        print(Fore.BLUE + f"\n📖 Opening article: {link}" + Style.RESET_ALL)
                        article_data = await scrape_article_page(context, link)
                        if article_data["title"] and (article_data["content"] or article_data["full_text"]):
                            data.append(article_data)
                            await show_progress(len(data), num_articles)
                        else:
                            print(Fore.YELLOW + f"\n⚠ Article missing content: {link}" + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.YELLOW + f"\n⚠ Error processing article {i+1}: {str(e)}" + Style.RESET_ALL)
                        continue

                if len(data) >= num_articles:
                    break

                # Try to go to next page
                next_button = await page.query_selector('a[aria-label*="Next"], a:has-text("Next"), .next a, .page-numbers.next')
                if next_button:
                    print(Fore.BLUE + f"\n⏩ Navigating to next page..." + Style.RESET_ALL)
                    await next_button.click()
                    await asyncio.sleep(2)
                    page_num += 1
                    consecutive_failed_pages = 0
                else:
                    print(Fore.YELLOW + "\nℹ️  No more pages available (no next button found)" + Style.RESET_ALL)
                    break
            except Exception as e:
                print(Fore.RED + f"\n⚠ Error loading page {page_num}: {str(e)}" + Style.RESET_ALL)
                consecutive_failed_pages += 1
                if consecutive_failed_pages >= 3:
                    break

        await context.close()
        await browser.close()
        print(Fore.GREEN + "\n✔ Scraping completed!" + Style.RESET_ALL)

        print(Fore.YELLOW + "="*60 + Style.RESET_ALL)
        print(Fore.CYAN + f"📊 Articles collected: {Fore.GREEN}{len(data)}" + Style.RESET_ALL)
        print(Fore.CYAN + f"📖 Pages processed: {Fore.GREEN}{page_num}" + Style.RESET_ALL)
        duration = (datetime.now() - start_time).total_seconds()
        print(Fore.CYAN + f"⏱️  Time taken: {Fore.GREEN}{duration:.2f} seconds" + Style.RESET_ALL)
        print(Fore.YELLOW + "="*60 + Style.RESET_ALL)

        if data:
            print(Fore.CYAN + "\n💾 Saving results..." + Style.RESET_ALL)
            final_data = data[:num_articles]
            for item in final_data:
                if 'link' in item:
                    item['link'] = clean_url(item['link'])
            df = pd.DataFrame(final_data)
            date_str = datetime.now().strftime("%Y-%m-%d")
            time_str = datetime.now().strftime("%H%M")
            article_count = len(final_data)
            base_name = f"microsoft_research_articles_{article_count}items_{date_str}_{time_str}"
            csv_file = os.path.join(csv_dir, f"{base_name}.csv")
            json_file = os.path.join(json_dir, f"{base_name}.json")
            df.to_csv(csv_file, index=False)
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, indent=2, ensure_ascii=False, separators=(',', ': '))
            csv_display_path = os.path.join("outputs", "microsoft-articles", "csv-files", f"{base_name}.csv")
            json_display_path = os.path.join("outputs", "microsoft-articles", "json-files", f"{base_name}.json")
            print(Fore.GREEN + f"\n✔ Files saved to organized directories:" + Style.RESET_ALL)
            print(Fore.WHITE + "   • CSV: " + Fore.CYAN + f"{csv_display_path}" + Style.RESET_ALL)
            print(Fore.WHITE + "   • JSON: " + Fore.MAGENTA + f"{json_display_path}" + Style.RESET_ALL)
            print(Fore.CYAN + "\n📋 Sample of collected articles:" + Style.RESET_ALL)
            for i, article in enumerate(final_data[:3]):
                print(Fore.WHITE + f"   {i+1}. " + Fore.GREEN + f"{article['title']}" + Style.RESET_ALL)
                print(Fore.WHITE + "      Author: " + Fore.CYAN + f"{article.get('author', 'N/A')}" + Style.RESET_ALL)
                print(Fore.WHITE + "      Date: " + Fore.YELLOW + f"{article.get('date', 'N/A')}" + Style.RESET_ALL)
                print(Fore.WHITE + "      Categories: " + Fore.MAGENTA + f"{', '.join(article.get('categories', []))}" + Style.RESET_ALL)
                print(Fore.WHITE + "      Content preview: " + Fore.WHITE + f"{article.get('content', 'N/A')[:100]}..." + Style.RESET_ALL)
            print(Fore.GREEN + f"\n✅ Successfully scraped {len(final_data)} articles with full content!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n⚠ No data was collected to save" + Style.RESET_ALL)
        print(Fore.YELLOW + "="*60 + Style.RESET_ALL)
        print(Fore.MAGENTA + "\n🎉 All done! Happy researching!" + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        asyncio.run(scrape_msresearch())
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n❌ Operation cancelled by user" + Style.RESET_ALL)
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n\n❌ An error occurred: {str(e)}" + Style.RESET_ALL)
        sys.exit(1)
    finally:
        try:
            input(Fore.BLUE + "\nPress Enter to exit..." + Style.RESET_ALL)
        except EOFError:
            print("\n")
            sys.exit(0)