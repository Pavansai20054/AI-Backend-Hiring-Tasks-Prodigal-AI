import asyncio
from playwright.async_api import async_playwright
import json
import csv
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
    print(Fore.MAGENTA + " • Scrapes government schemes with title, URL, ministry and description")
    print(Fore.MAGENTA + " • Saves results in CSV and JSON formats")
    print(Fore.MAGENTA + " • Interactive progress tracking")
    print(Fore.GREEN + "="*60 + Style.RESET_ALL)

def create_output_directories():
    """Use the existing output directory structure"""
    # Get the current script directory (article_scheme_scraper folder)
    script_dir = Path(__file__).parent
    
    # Go up one level to project root, then to existing outputs folder
    project_root = script_dir.parent
    csv_output_path = project_root / "outputs" / "myscehme-schemes" / "csv-files"
    json_output_path = project_root / "outputs" / "myscehme-schemes" / "json-files"
    
    # Ensure directories exist (they should already exist)
    csv_output_path.mkdir(parents=True, exist_ok=True)
    json_output_path.mkdir(parents=True, exist_ok=True)
    
    print(Fore.CYAN + f"📁 Using existing output directories:" + Style.RESET_ALL)
    print(Fore.WHITE + "   • CSV: " + Fore.GREEN + "outputs/myscehme-schemes/csv-files" + Style.RESET_ALL)
    print(Fore.WHITE + "   • JSON: " + Fore.GREEN + "outputs/myscehme-schemes/json-files" + Style.RESET_ALL)
    
    return csv_output_path, json_output_path

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

BASE_URL = "https://www.myscheme.gov.in/search"

async def extract_schemes_from_page(page):
    try:
        # Further reduced timeout from 2000 to 1000
        await page.wait_for_selector('h2 a', timeout=1000)
    except Exception:
        print(Fore.YELLOW + "⚠ Could not find scheme listings" + Style.RESET_ALL)
        return []

    scheme_blocks = await page.query_selector_all('div.flex.flex-row.items-center.justify-between')
    results = []

    for block in scheme_blocks:
        try:
            # Ultra-fast scrolling with instant behavior and minimal delay
            await page.evaluate("(el) => el.scrollIntoView({behavior: 'instant', block: 'center'})", block)
            await asyncio.sleep(0.02)  # Reduced from 0.05 to 0.02 for much faster scrolling

            # Title & URL
            title_elem = await block.query_selector('h2 a')
            if not title_elem:
                continue
                
            # Parallelize data extraction where possible
            title_future = title_elem.inner_text()
            url_future = title_elem.get_attribute('href')
            title, url = await asyncio.gather(title_future, url_future)
            
            url = f"https://www.myscheme.gov.in{url}" if url else None

            # Ministry
            ministry = None
            ministry_elem = await block.query_selector('h2.mt-3')
            if ministry_elem:
                ministry = (await ministry_elem.inner_text()).strip()

            # Description
            description = None
            desc_elem = await block.query_selector('span.mt-3')
            if desc_elem:
                description = (await desc_elem.inner_text()).strip()

            results.append({
                "title": title.strip(),
                "url": url,
                "ministry": ministry,
                "description": description,
            })
        except Exception as e:
            continue

    return results

async def scrape_myscheme():
    print_header()
    
    # Create output directories
    csv_output_path, json_output_path = create_output_directories()
    
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
    all_results = []
    current_page = 1
    consecutive_failed_pages = 0
    
    async with async_playwright() as p:
        # Much faster browser launch - removed slow_mo, optimized settings
        print(Fore.BLUE + "\n🖥️  Launching browser... (this may take a moment)" + Style.RESET_ALL)
        browser = await p.chromium.launch(
            headless=False,
            # Removed slow_mo completely for faster execution
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
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            # Faster loading optimizations
            java_script_enabled=True,
            bypass_csp=True,
            ignore_https_errors=True,
            # Disable images and CSS for faster loading
            # extra_http_headers={'Accept-Language': 'en-US,en;q=0.9'}
        )
        page = await context.new_page()

        # Ultra-fast navigation with very aggressive timeout reduction
        print(Fore.BLUE + "\n🌐 Navigating to MyScheme.gov.in..." + Style.RESET_ALL)
        try:
            await page.goto(BASE_URL, timeout=5000)  # Reduced from 8000 to 5000
            await page.wait_for_load_state("domcontentloaded")  # Faster than "networkidle"
            print(Fore.GREEN + "✔ Successfully loaded the scheme search page" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"✖ Failed to load page: {str(e)}" + Style.RESET_ALL)
            await browser.close()
            return

        # Scraping process with animated progress
        print(Fore.CYAN + "\n🔍 Scraping schemes..." + Style.RESET_ALL)
        
        while len(all_results) < num_schemes and consecutive_failed_pages < 3:
            print(Fore.BLUE + f"\n📄 Processing page {current_page}..." + Style.RESET_ALL)
            
            page_results = await extract_schemes_from_page(page)
            
            if not page_results:
                print(Fore.YELLOW + "⚠ No schemes found on this page." + Style.RESET_ALL)
                consecutive_failed_pages += 1
                if consecutive_failed_pages >= 3:
                    print(Fore.YELLOW + "⚠ Too many consecutive failed pages, stopping..." + Style.RESET_ALL)
                    break
                continue
            
            # Reset failed pages counter if we found results
            consecutive_failed_pages = 0
            
            for scheme in page_results:
                if scheme not in all_results:
                    all_results.append(scheme)
                    await show_progress(len(all_results), num_schemes)
                    if len(all_results) >= num_schemes:
                        break

            if len(all_results) >= num_schemes:
                break

            # Ultra-fast pagination with minimal waits
            try:
                next_page = current_page + 1
                page_btn = await page.query_selector(f'li:has-text("{next_page}")')
                
                if page_btn:
                    print(Fore.BLUE + f"\n⏩ Clicking page {next_page}..." + Style.RESET_ALL)
                    await page_btn.click()
                    # Ultra-fast wait time and simplified logic
                    try:
                        await page.wait_for_selector('div.flex.flex-row', timeout=800)  # Reduced from 1500
                        await asyncio.sleep(0.2)  # Reduced from 0.5 for faster page loads
                    except:
                        # If wait_for_selector fails, just add a tiny delay
                        await asyncio.sleep(0.5)  # Reduced from 1
                    
                    current_page += 1
                    print(Fore.GREEN + f"✔ Successfully navigated to page {current_page}" + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + "\nℹ️  No more pages available (no next button found)" + Style.RESET_ALL)
                    break
            except Exception as e:
                print(Fore.RED + f"\n⚠ Error navigating to next page: {str(e)}" + Style.RESET_ALL)
                consecutive_failed_pages += 1
                if consecutive_failed_pages >= 3:
                    print(Fore.YELLOW + "⚠ Too many pagination failures, stopping..." + Style.RESET_ALL)
                    break

        # Close browser
        await context.close()
        await browser.close()
        print(Fore.GREEN + "\n✔ Scraping completed!" + Style.RESET_ALL)

        # Final output
        print(Fore.GREEN + r"""
[38;5;208m   ╔═╗╔═╗╦═╗╔═╗╔═╗╔═╗╦╔╗╔╔═╗  ╔═╗╔═╗╔╦╗╔═╗╦  ╔═╗╔╦╗╔═╗╔╦╗
[38;5;15m   ╚═╗║  ╠╦╝╠═╣╠═╝╠═╝║║║║║ ╦  ║  ║ ║║║║╠═╝║  ║╣  ║ ║╣  ║║
[38;5;40m   ╚═╝╚═╝╩╚═╩ ╩╩  ╩  ╩╝╚╝╚═╝  ╚═╝╚═╝╩ ╩╩  ╩═╝╚═╝ ╩ ╚═╝═╩╝
        """ + Style.RESET_ALL)
        
        print(Fore.YELLOW + "="*60 + Style.RESET_ALL)
        print(Fore.CYAN + f"📊 Schemes collected: {Fore.GREEN}{len(all_results)}" + Style.RESET_ALL)
        print(Fore.CYAN + f"📖 Pages processed: {Fore.GREEN}{current_page}" + Style.RESET_ALL)
        
        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        print(Fore.CYAN + f"⏱️  Time taken: {Fore.GREEN}{duration:.2f} seconds" + Style.RESET_ALL)
        print(Fore.YELLOW + "="*60 + Style.RESET_ALL)
        
        # Save results
        if all_results:
            print(Fore.CYAN + "\n💾 Saving results..." + Style.RESET_ALL)
            # Limit to requested number of schemes
            final_data = all_results[:num_schemes]

            # Create meaningful filenames
            date_str = datetime.now().strftime("%Y-%m-%d")
            time_str = datetime.now().strftime("%H%M")
            scheme_count = len(final_data)
            
            # Generate descriptive filename
            base_name = f"myscheme_gov_schemes_{scheme_count}items_{date_str}_{time_str}"
            
            # Create full file paths using the designated directories
            csv_file = csv_output_path / f"{base_name}.csv"
            json_file = json_output_path / f"{base_name}.json"

            # Save JSON
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(final_data, f, indent=2, ensure_ascii=False)

            # Save CSV
            with open(csv_file, "w", encoding="utf-8", newline='') as csvfile:
                fieldnames = ["title", "url", "ministry", "description"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
                writer.writeheader()
                writer.writerows(final_data)

            print(Fore.GREEN + f"\n✔ Files saved:" + Style.RESET_ALL)
            print(Fore.WHITE + "   • " + Fore.GREEN + f"outputs/myscehme-schemes/csv-files/{csv_file.name}" + Style.RESET_ALL)
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