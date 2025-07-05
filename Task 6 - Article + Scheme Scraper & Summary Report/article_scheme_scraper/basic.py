import asyncio
from playwright.async_api import async_playwright
import random

async def human_like_scroll(page):
    """Scroll through the page like a human"""
    viewport_height = await page.evaluate("window.innerHeight")
    scroll_height = await page.evaluate("document.body.scrollHeight")
    current_pos = 0
    
    while current_pos < scroll_height - viewport_height:
        # Random scroll distance and delay
        scroll_step = random.randint(200, 500)
        current_pos += scroll_step
        await page.evaluate(f"window.scrollTo(0, {current_pos})")
        await asyncio.sleep(random.uniform(0.3, 1.2))

async def scrape_blogs(num_blogs):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Set realistic viewport
        await page.set_viewport_size({"width": 1280, "height": 800})
        
        # Navigate to blog page
        print("Loading blog page...")
        await page.goto("https://www.microsoft.com/en-us/research/blog/", timeout=60000)
        await asyncio.sleep(random.uniform(2, 4))  # Human-like delay
        
        # Wait for and collect blog links
        print("Finding blog posts...")
        try:
            await page.wait_for_selector('article a[href]', timeout=15000)
            blog_links = await page.query_selector_all('article a[href]')
            
            if not blog_links:
                print("No blog links found using 'article a[href]' selector")
                return
            
            num_blogs = min(num_blogs, len(blog_links))
            print(f"Found {len(blog_links)} posts. Scraping {num_blogs}...")
            
            for i in range(num_blogs):
                print(f"\nProcessing blog {i+1}/{num_blogs}")
                
                # Scroll to the blog link
                await blog_links[i].scroll_into_view_if_needed()
                await asyncio.sleep(random.uniform(0.5, 1.5))
                
                # Click the blog post
                href = await blog_links[i].get_attribute('href')
                print(f"Opening: {href}")
                await blog_links[i].click()
                await page.wait_for_load_state('networkidle')
                
                # Scroll through the article
                print("Reading article...")
                await human_like_scroll(page)
                await asyncio.sleep(random.uniform(1, 3))
                
                # Return to main page
                print("Returning to blog list...")
                await page.go_back()
                await page.wait_for_selector('article a[href]')
                await asyncio.sleep(random.uniform(2, 4))
                
                # Refresh blog links
                blog_links = await page.query_selector_all('article a[href]')
                
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            await browser.close()
            print("Finished scraping.")

if __name__ == "__main__":
    try:
        num_blogs = int(input("Enter number of blogs to scrape: "))
        asyncio.run(scrape_blogs(num_blogs))
    except ValueError:
        print("Please enter a valid number")