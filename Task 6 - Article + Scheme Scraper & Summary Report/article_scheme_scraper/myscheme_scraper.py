import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime
from colorama import Fore, Style, init
import sys
import os
from pathlib import Path

# Initialize colorama
init(autoreset=True)

def clear_console():
    """Clear console based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print colorful header"""
    clear_console()
    print(Fore.GREEN + "  __  ____     " + Fore.MAGENTA + "_______  _____ _    _ ______ __  __ ______    _____  _____ _____            _____  ______ _____  ")
    print(Fore.GREEN + " |  \/  \ \   / /" + Fore.MAGENTA + " ____|/ ____| |  | |  ____|  \/  |  ____|  / ____|/ ____|  __ \     /\   |  __ \|  ____|  __ \ ")
    print(Fore.GREEN + " | \  / |\ \_/ /" + Fore.MAGENTA + " (___ | |    | |__| | |__  | \  / | |__    | (___ | |    | |__) |   /  \  | |__) | |__  | |__) |")
    print(Fore.GREEN + " | |\/| | \   / " + Fore.MAGENTA + "\___ \| |    |  __  |  __| | |\/| |  __|    \___ \| |    |  _  /   / /\ \ |  ___/|  __| |  _  / ")
    print(Fore.GREEN + " | |  | |  | |  " + Fore.MAGENTA + "____) | |____| |  | | |____| |  | | |____   ____) | |____| | \ \  / ____ \| |    | |____| | \ \ ")
    print(Fore.GREEN + " |_|  |_|  |_| |" + Fore.MAGENTA + "_____/ \_____|_|  |_|______|_|  |_|______| |_____/ \_____|_|  \_\/_/    \_\_|    |______|_|  \_\ ")
    print(Fore.MAGENTA + "                                                                                                                ")
    print(Style.RESET_ALL)
    print(Fore.YELLOW + " MyScheme Government Scheme Scraper " + Style.RESET_ALL)
    print(Fore.GREEN + "="*60 + Style.RESET_ALL)
    print(Fore.MAGENTA + " • Scrapes government schemes with title, URL, and content")
    print(Fore.MAGENTA + " • Saves results in JSON format")
    print(Fore.MAGENTA + " • Interactive progress tracking")
    print(Fore.GREEN + "="*60 + Style.RESET_ALL)

def create_output_directory():
    """Create output directory structure"""
    # Get the current script directory (article_scheme_scraper folder)
    script_dir = Path(__file__).parent
    
    # Go up one level to project root, then to outputs folder
    project_root = script_dir.parent
    json_output_path = project_root / "outputs" / "myscehme-schemes" / "json-files"
    
    # Ensure directory exists
    json_output_path.mkdir(parents=True, exist_ok=True)
    
    print(Fore.CYAN + f"📁 Using output directory:" + Style.RESET_ALL)
    print(Fore.WHITE + "   • JSON: " + Fore.GREEN + "outputs/myscehme-schemes/json-files" + Style.RESET_ALL)
    
    return json_output_path

async def show_progress(current, total):
    """Animated progress bar"""
    bar_length = 30
    progress = float(current)/float(total)
    block = int(round(bar_length * progress))
    percent = round(progress * 100, 2)
    
    progress_bar = (Fore.GREEN + "█" * block + 
                   Fore.MAGENTA + "░" * (bar_length - block) + 
                   Style.RESET_ALL)
    
    sys.stdout.write(f"\r[{progress_bar}] {percent}% ({current}/{total} schemes)")
    sys.stdout.flush()

async def scrape_myscheme():
    print_header()
    
    # Create output directory
    json_output_path = create_output_directory()
    
    # Get user input with validation and emoji feedback
    while True:
        try:
            num_schemes = int(input(Fore.BLUE + "\n🔢 How many schemes would you like to scrape? (Enter positive Integer): " + Style.RESET_ALL))
            if num_schemes > 0:
                print(Fore.GREEN + f"✅ Great! I'll fetch {num_schemes} schemes for you!" + Style.RESET_ALL)
                break
            print(Fore.RED + "❌ Please enter a positive number." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "❌ Invalid input. Please enter a number." + Style.RESET_ALL)
    
    print(Fore.CYAN + "\n🚀 Starting scrape..." + Style.RESET_ALL)
    start_time = datetime.now()
    data = []
    seen_titles = set()
    scraped = 0
    
    async with async_playwright() as p:
        # Browser launch with optimized settings
        print(Fore.BLUE + "\n🖥️  Launching browser... (this may take a moment)" + Style.RESET_ALL)
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-dev-shm-usage',
                '--disable-extensions',
                '--disable-gpu',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding'
            ]
        )
        
        page = await browser.new_page(
            viewport={"width": 1280, "height": 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )

        # Navigation
        print(Fore.BLUE + "\n🌐 Navigating to MyScheme.gov.in..." + Style.RESET_ALL)
        try:
            await page.goto("https://www.myscheme.gov.in/search", timeout=5000)
            await page.wait_for_load_state("domcontentloaded")
            print(Fore.GREEN + "✔ Successfully loaded the scheme search page" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"✖ Failed to load page: {str(e)}" + Style.RESET_ALL)
            await browser.close()
            return

        # Scraping process with animated progress
        print(Fore.CYAN + "\n🔍 Scraping schemes..." + Style.RESET_ALL)
        
        current_page = 1
        while scraped < num_schemes:
            print(Fore.BLUE + f"\n📄 Processing page {current_page}..." + Style.RESET_ALL)
            
            cards = await page.query_selector_all('div.rounded-xl.shadow-md.overflow-hidden')
            for card in cards:
                if scraped >= num_schemes:
                    break
                    
                title, link, content = "", "", ""
                title_el = await card.query_selector('a.block.text-lg.leading-tight.font-medium')
                if title_el:
                    title = (await title_el.inner_text()).strip()
                    # Avoid duplicate scraping due to stale DOM or slow page change!
                    if title in seen_titles:
                        continue
                    seen_titles.add(title)
                    link = await title_el.get_attribute('href')
                    if link and link.startswith("/"):
                        link = f"https://www.myscheme.gov.in{link}"
                        
                if link:
                    try:
                        detail_page = await browser.new_page()
                        await detail_page.goto(link)
                        await detail_page.wait_for_load_state("domcontentloaded")
                        await detail_page.wait_for_timeout(1000)
                        content_el = await detail_page.query_selector('div.prose')
                        if not content_el:
                            content_el = await detail_page.query_selector('main')
                        if content_el:
                            content = (await content_el.inner_text()).strip()
                        await detail_page.close()
                    except Exception:
                        content = ""
                        
                data.append({
                    "title": title,
                    "url": link,
                    "content": content
                })
                scraped += 1
                await show_progress(scraped, num_schemes)

            # Pagination: go to next page if needed
            if scraped < num_schemes:
                next_page_num = current_page + 1
                next_btn = await page.query_selector(
                    f'li.h-8.w-8.text-darkblue-900.flex.items-center.justify-center.text-base.mx-1.rounded-full:has-text("{next_page_num}")'
                )
                if next_btn:
                    first_title_el = await page.query_selector('div.rounded-xl.shadow-md.overflow-hidden a.block.text-lg.leading-tight.font-medium')
                    first_title = await first_title_el.inner_text() if first_title_el else ""
                    await next_btn.click()
                    await page.wait_for_function(
                        f'''
                        () => {{
                            const el = document.querySelector('div.rounded-xl.shadow-md.overflow-hidden a.block.text-lg.leading-tight.font-medium');
                            return el && el.innerText.trim() !== `{first_title.strip()}`;
                        }}
                        ''',
                        timeout=10000
                    )
                    current_page += 1
                    print(Fore.GREEN + f"✔ Successfully navigated to page {current_page}" + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + "\nℹ️  No more pages available" + Style.RESET_ALL)
                    break

        # Close browser
        await browser.close()
        print(Fore.GREEN + "\n✔ Scraping completed!" + Style.RESET_ALL)

        # Final output
        print(Fore.GREEN + r"""
[38;5;208m   ╔═╗╔═╗╦═╗╔═╗╔═╗╔═╗╦╔╗╔╔═╗  ╔═╗╔═╗╔╦╗╔═╗╦  ╔═╗╔╦╗╔═╗╔╦╗
[38;5;15m   ╚═╗║  ╠╦╝╠═╣╠═╝╠═╝║║║║║ ╦  ║  ║ ║║║║╠═╝║  ║╣  ║ ║╣  ║║
[38;5;40m   ╚═╝╚═╝╩╚═╩ ╩╩  ╩  ╩╝╚╝╚═╝  ╚═╝╚═╝╩ ╩╩  ╩═╝╚═╝ ╩ ╚═╝═╩╝
        """ + Style.RESET_ALL)
        
        print(Fore.YELLOW + "="*60 + Style.RESET_ALL)
        print(Fore.CYAN + f"📊 Schemes collected: {Fore.GREEN}{len(data)}" + Style.RESET_ALL)
        print(Fore.CYAN + f"📖 Pages processed: {Fore.GREEN}{current_page}" + Style.RESET_ALL)
        
        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        print(Fore.CYAN + f"⏱️  Time taken: {Fore.GREEN}{duration:.2f} seconds" + Style.RESET_ALL)
        print(Fore.YELLOW + "="*60 + Style.RESET_ALL)
        
        # Save results
        if data:
            print(Fore.CYAN + "\n💾 Saving results..." + Style.RESET_ALL)
            # Limit to requested number of schemes
            final_data = data[:num_schemes]

            # Create meaningful filename
            date_str = datetime.now().strftime("%Y-%m-%d")
            time_str = datetime.now().strftime("%H%M")
            scheme_count = len(final_data)
            
            # Generate descriptive filename
            base_name = f"myscheme_gov_schemes_{scheme_count}items_{date_str}_{time_str}"
            
            # Create full file path using the designated directory
            json_file = json_output_path / f"{base_name}.json"

            # Save JSON
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(final_data, f, indent=2, ensure_ascii=False)

            print(Fore.GREEN + f"\n✔ File saved:" + Style.RESET_ALL)
            print(Fore.WHITE + "   • " + Fore.GREEN + f"outputs/myscehme-schemes/json-files/{json_file.name}" + Style.RESET_ALL)
            
            # Show sample of collected data
            print(Fore.CYAN + "\n📋 Sample of collected schemes:" + Style.RESET_ALL)
            for i, scheme in enumerate(final_data[:3]):
                print(Fore.WHITE + f"   {i+1}. " + Fore.GREEN + f"{scheme['title'][:80]}..." + Style.RESET_ALL)
        else:
            print(Fore.RED + "\n⚠ No data was collected to save" + Style.RESET_ALL)
            
        print(Fore.YELLOW + "="*60 + Style.RESET_ALL)
        print(Fore.MAGENTA + "\n🎉 All done! Happy scheme exploring!" + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        asyncio.run(scrape_myscheme())
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