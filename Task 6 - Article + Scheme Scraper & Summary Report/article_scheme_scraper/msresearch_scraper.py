import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime
from colorama import Fore, Style, init
import sys
import os
import json

# Initialize colorama
init(autoreset=True)

def clear_console():
    """Clear console based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print colorful header"""
    clear_console()
    print(Fore.CYAN + r"""
[38;5;196m╔╦╗[38;5;226m╦[38;5;39m╔═╗[38;5;196m╦═╗[38;5;40m╔═╗[38;5;226m╔═╗[38;5;196m╔═╗[38;5;40m╔═╗[38;5;226m╔╦╗  [38;5;196m╦═╗[38;5;40m╔═╗[38;5;226m╔═╗[38;5;39m╔═╗[38;5;196m╔═╗[38;5;40m╦═╗[38;5;226m╔═╗[38;5;39m╦ ╦  [38;5;196m╔╗ ╦  [38;5;40m╔═╗[38;5;226m╔═╗  [38;5;196m╔═╗[38;5;40m╔═╗[38;5;226m╦═╗[38;5;39m╔═╗[38;5;196m╔═╗[38;5;40m╔═╗[38;5;226m╦═╗
[38;5;196m║║║[38;5;226m║║  [38;5;39m╠╦╝[38;5;196m║ ║[38;5;40m╚═╗[38;5;226m║ ║[38;5;196m╠╣  [38;5;40m║   [38;5;226m╠╦╝[38;5;39m║╣ [38;5;196m╚═╗[38;5;40m║╣ [38;5;226m╠═╣[38;5;39m╠╦╝[38;5;196m║  [38;5;40m╠═╣  [38;5;226m╠╩╗[38;5;39m║  [38;5;196m║ ║[38;5;40m║ ╦  [38;5;226m╚═╗[38;5;39m║  [38;5;196m╠╦╝[38;5;40m╠═╣[38;5;226m╠═╝[38;5;39m║╣ [38;5;196m╠╦╝
[38;5;196m╩ ╩[38;5;226m╩╚═╝[38;5;39m╩╚═[38;5;196m╚═╝[38;5;40m╚═╝[38;5;226m╚═╝[38;5;196m╚   [38;5;40m╩   [38;5;226m╩╚═[38;5;39m╚═╝[38;5;196m╚═╝[38;5;40m╚═╝[38;5;226m╩ ╩[38;5;39m╩╚═[38;5;196m╚═╝[38;5;40m╩ ╩  [38;5;226m╚═╝[38;5;39m╩═╝[38;5;196m╚═╝[38;5;40m╚═╝  [38;5;226m╚═╝[38;5;39m╚═╝[38;5;196m╩╚═[38;5;40m╩ ╩[38;5;226m╩  [38;5;39m╚═╝[38;5;196m╩╚═
    """)
    print(Fore.YELLOW + " Microsoft Research Blog Scraper " + Style.RESET_ALL)
    print(Fore.GREEN + "="*60 + Style.RESET_ALL)
    print(Fore.MAGENTA + " • Scrapes articles with title, link, and description")
    print(Fore.MAGENTA + " • Saves results in CSV and JSON formats")
    print(Fore.MAGENTA + " • Interactive progress tracking")
    print(Fore.GREEN + "="*60 + Style.RESET_ALL)

def create_output_directories():
    """Create output directories if they don't exist"""
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the output paths relative to the script location
    outputs_dir = os.path.join(script_dir, "..", "outputs", "microsoft-articles")
    csv_dir = os.path.join(outputs_dir, "csv-files")
    json_dir = os.path.join(outputs_dir, "json-files")
    
    # Create directories if they don't exist
    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)
    
    # Create clean relative paths for display
    csv_display_path = os.path.join("outputs", "microsoft-articles", "csv-files")
    json_display_path = os.path.join("outputs", "microsoft-articles", "json-files")
    
    print(Fore.CYAN + "✔ Output directories created/verified:" + Style.RESET_ALL)
    print(Fore.WHITE + "   • CSV: " + Fore.GREEN + f"{csv_display_path}" + Style.RESET_ALL)
    print(Fore.WHITE + "   • JSON: " + Fore.GREEN + f"{json_display_path}" + Style.RESET_ALL)
    
    return csv_dir, json_dir

async def show_progress(current, total):
    """Animated progress bar"""
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
    """Clean and validate URL format"""
    if not url or url == "No link":
        return url
    
    # Remove any escaped slashes
    url = url.replace('\\/', '/')
    
    # Ensure proper URL format
    if url.startswith('/'):
        url = f"https://www.microsoft.com{url}"
    elif not url.startswith('http'):
        url = f"https://www.microsoft.com/en-us/research/blog/{url}"
    
    return url

async def scrape_msresearch():
    print_header()
    
    # Create output directories
    csv_dir, json_dir = create_output_directories()
    
    # Get user input with validation and emoji feedback
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
        # Browser setup with emoji feedback
        print(Fore.BLUE + "\n🖥️  Launching browser... (this may take a moment)" + Style.RESET_ALL)
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navigation with timeout handling
        print(Fore.BLUE + "\n🌐 Navigating to Microsoft Research Blog..." + Style.RESET_ALL)
        try:
            await page.goto("https://www.microsoft.com/en-us/research/blog/", timeout=30000)
            print(Fore.GREEN + "✔ Successfully loaded the blog page" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"✖ Failed to load page: {str(e)}" + Style.RESET_ALL)
            await browser.close()
            return

        # Scraping process with animated progress
        print(Fore.CYAN + "\n🔍 Scraping articles..." + Style.RESET_ALL)
        page_num = 1
        articles_on_current_page = 0
        consecutive_failed_pages = 0
        
        while len(data) < num_articles and consecutive_failed_pages < 3:
            try:
                # Wait for content to load
                await page.wait_for_selector('article', timeout=10000)
                
                # Get all articles on current page
                articles = await page.query_selector_all('article')
                articles_found_on_page = 0
                
                print(Fore.BLUE + f"\n📄 Processing page {page_num} ({len(articles)} articles found)..." + Style.RESET_ALL)
                
                for i, article in enumerate(articles):
                    if len(data) >= num_articles:
                        break
                    
                    try:
                        # Scroll article into view safely
                        try:
                            await article.scroll_into_view_if_needed()
                            await asyncio.sleep(0.1)  # Small delay for rendering
                        except Exception:
                            pass  # Continue if scroll fails
                        
                        # Enhanced data extraction with multiple fallback selectors
                        title_selectors = [
                            'h2 a', 'h2', 'h3 a', 'h3', 'h1 a', 'h1',
                            '.entry-title a', '.entry-title', 
                            '[data-testid="title"]', '.title a', '.title'
                        ]
                        
                        link_selectors = [
                            'h2 a', 'h3 a', 'h1 a', 'a[href*="/research/blog/"]',
                            '.entry-title a', 'a[href*="/blog/"]', 'a:first-of-type'
                        ]
                        
                        desc_selectors = [
                            'p', '.excerpt', '.summary', '.description',
                            '.entry-content p', '.post-excerpt', 
                            '[data-testid="description"]'
                        ]
                        
                        # Extract title
                        title = "No title"
                        for selector in title_selectors:
                            try:
                                title_elem = await article.query_selector(selector)
                                if title_elem:
                                    title_text = await title_elem.inner_text()
                                    if title_text and title_text.strip():
                                        title = title_text.strip()
                                        break
                            except:
                                continue
                        
                        # Extract link
                        link = "No link"
                        for selector in link_selectors:
                            try:
                                link_elem = await article.query_selector(selector)
                                if link_elem:
                                    href = await link_elem.get_attribute('href')
                                    if href:
                                        # Clean and format URL properly
                                        link = clean_url(href)
                                        break
                            except:
                                continue
                        
                        # Extract description
                        description = "No description"
                        for selector in desc_selectors:
                            try:
                                desc_elem = await article.query_selector(selector)
                                if desc_elem:
                                    desc_text = await desc_elem.inner_text()
                                    if desc_text and desc_text.strip() and len(desc_text.strip()) > 20:
                                        description = desc_text.strip()[:500]  # Limit length
                                        break
                            except:
                                continue
                        
                        # Only add if we have meaningful data
                        if title != "No title" and link != "No link":
                            data.append({
                                "title": title,
                                "link": link,
                                "description": description
                            })
                            articles_found_on_page += 1
                            
                            # Update progress bar
                            await show_progress(len(data), num_articles)
                            await asyncio.sleep(0.05)
                        
                    except Exception as e:
                        print(Fore.YELLOW + f"\n⚠ Error processing article {i+1}: {str(e)}" + Style.RESET_ALL)
                        continue
                
                print(Fore.GREEN + f"\n✔ Extracted {articles_found_on_page} articles from page {page_num}" + Style.RESET_ALL)
                
                # If we have enough articles, break
                if len(data) >= num_articles:
                    break
                
                # If no articles found on this page, increment failed counter
                if articles_found_on_page == 0:
                    consecutive_failed_pages += 1
                    print(Fore.YELLOW + f"⚠ No new articles found on page {page_num}" + Style.RESET_ALL)
                else:
                    consecutive_failed_pages = 0
                
                # Try to navigate to next page with improved selectors
                try:
                    # Multiple pagination selector strategies
                    next_selectors = [
                        'a[aria-label*="Next"]',
                        'a[aria-label*="next"]', 
                        'a:has-text("Next")',
                        'a:has-text("next")',
                        'a:has-text(">")',
                        '.next a',
                        '.pagination-next a',
                        '.nav-next a',
                        '.pager-next a',
                        'a[rel="next"]',
                        '.wp-pagenavi a:last-child',
                        '.page-numbers:last-child',
                        # Numeric pagination - try to find next page number
                        f'a:has-text("{page_num + 1}")'
                    ]
                    
                    next_button = None
                    used_selector = None
                    
                    for selector in next_selectors:
                        try:
                            next_button = await page.query_selector(selector)
                            if next_button:
                                # Verify it's actually clickable and not disabled
                                is_disabled = await next_button.evaluate('el => el.disabled || el.classList.contains("disabled") || el.getAttribute("aria-disabled") === "true"')
                                if not is_disabled:
                                    used_selector = selector
                                    break
                        except:
                            continue
                    
                    if next_button and used_selector:
                        print(Fore.BLUE + f"\n⏩ Found next button with selector: {used_selector}" + Style.RESET_ALL)
                        print(Fore.BLUE + f"   Navigating to page {page_num + 1}..." + Style.RESET_ALL)
                        
                        # Store current state
                        current_url = page.url
                        current_articles_count = len(await page.query_selector_all('article'))
                        
                        try:
                            # Try different click strategies
                            await next_button.click(timeout=5000)
                        except:
                            try:
                                await next_button.dispatch_event('click')
                            except:
                                # Try to get href and navigate directly
                                href = await next_button.get_attribute('href')
                                if href:
                                    if href.startswith('/'):
                                        href = f"https://www.microsoft.com{href}"
                                    elif not href.startswith('http'):
                                        href = f"https://www.microsoft.com/en-us/research/blog/{href}"
                                    await page.goto(href, timeout=10000)
                        
                        # Wait for page change with multiple strategies
                        page_changed = False
                        try:
                            # Wait for URL change or content change
                            await page.wait_for_function(
                                f'window.location.href !== "{current_url}" || document.querySelectorAll("article").length !== {current_articles_count}', 
                                timeout=5000
                            )
                            page_changed = True
                        except:
                            try:
                                await page.wait_for_load_state('networkidle', timeout=5000)
                                page_changed = True
                            except:
                                try:
                                    await page.wait_for_selector('article', timeout=5000)
                                    page_changed = True
                                except:
                                    pass
                        
                        if page_changed:
                            # Additional wait for content to render
                            await asyncio.sleep(1)
                            page_num += 1
                            print(Fore.GREEN + f"✔ Successfully navigated to page {page_num}" + Style.RESET_ALL)
                        else:
                            print(Fore.YELLOW + f"⚠ Navigation might have failed - continuing anyway" + Style.RESET_ALL)
                            consecutive_failed_pages += 1
                    else:
                        print(Fore.YELLOW + "\nℹ️  No more pages available (no next button found)" + Style.RESET_ALL)
                        break
                        
                except Exception as e:
                    print(Fore.RED + f"\n⚠ Error during pagination: {str(e)}" + Style.RESET_ALL)
                    consecutive_failed_pages += 1
                    if consecutive_failed_pages >= 3:
                        print(Fore.YELLOW + "⚠ Too many pagination failures, stopping..." + Style.RESET_ALL)
                        break
                    
            except Exception as e:
                print(Fore.RED + f"\n⚠ Error loading page {page_num}: {str(e)}" + Style.RESET_ALL)
                consecutive_failed_pages += 1
                if consecutive_failed_pages >= 3:
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
        print(Fore.CYAN + f"📊 Articles collected: {Fore.GREEN}{len(data)}" + Style.RESET_ALL)
        print(Fore.CYAN + f"📖 Pages processed: {Fore.GREEN}{page_num}" + Style.RESET_ALL)
        
        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        print(Fore.CYAN + f"⏱️  Time taken: {Fore.GREEN}{duration:.2f} seconds" + Style.RESET_ALL)
        print(Fore.YELLOW + "="*60 + Style.RESET_ALL)
        
        # Save results
        if data:
            print(Fore.CYAN + "\n💾 Saving results..." + Style.RESET_ALL)
            # Limit to requested number of articles
            final_data = data[:num_articles]
            
            # Additional URL cleaning before saving
            for item in final_data:
                if 'link' in item:
                    item['link'] = clean_url(item['link'])
            
            df = pd.DataFrame(final_data)

            # Create meaningful filenames
            date_str = datetime.now().strftime("%Y-%m-%d")
            time_str = datetime.now().strftime("%H%M")
            article_count = len(final_data)
            
            # Generate descriptive filename
            base_name = f"microsoft_research_articles_{article_count}items_{date_str}_{time_str}"
            
            # Create full file paths using the organized directories
            csv_file = os.path.join(csv_dir, f"{base_name}.csv")
            json_file = os.path.join(json_dir, f"{base_name}.json")

            # Save CSV file
            df.to_csv(csv_file, index=False)
            
            # Save JSON file with proper URL formatting (NO ESCAPED SLASHES)
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, indent=2, ensure_ascii=False, separators=(',', ': '))

            # Create clean relative paths for display
            csv_display_path = os.path.join("outputs", "microsoft-articles", "csv-files", f"{base_name}.csv")
            json_display_path = os.path.join("outputs", "microsoft-articles", "json-files", f"{base_name}.json")

            print(Fore.GREEN + f"\n✔ Files saved to organized directories:" + Style.RESET_ALL)
            print(Fore.WHITE + "   • CSV: " + Fore.CYAN + f"{csv_display_path}" + Style.RESET_ALL)
            print(Fore.WHITE + "   • JSON: " + Fore.MAGENTA + f"{json_display_path}" + Style.RESET_ALL)
            
            # Show sample of collected data WITHOUT URLs
            print(Fore.CYAN + "\n📋 Sample of collected articles:" + Style.RESET_ALL)
            for i, article in enumerate(final_data[:3]):
                print(Fore.WHITE + f"   {i+1}. " + Fore.GREEN + f"{article['title']}" + Style.RESET_ALL)
                
            print(Fore.GREEN + f"\n✅ Successfully scraped {len(final_data)} articles!" + Style.RESET_ALL)
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