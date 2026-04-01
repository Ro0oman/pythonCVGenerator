import asyncio
from playwright.async_api import async_playwright
import random
import json
import os
import hashlib

CACHE_DIR = ".cache"
CACHE_FILE = os.path.join(CACHE_DIR, "job_cache.json")

def get_cache_key(url):
    return hashlib.md5(url.encode()).hexdigest()

def get_cached_job(url):
    if not os.path.exists(CACHE_FILE):
        return None
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
        return cache.get(get_cache_key(url))

def save_to_cache(url, data):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
            
    cache[get_cache_key(url)] = data
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=4)

async def scrape_job_offer(url: str):
    """
    Scrapes a job offer from a given URL using Playwright.
    Includes persistent caching to save tokens and time.
    """
    cached = get_cached_job(url)
    if cached:
        print(f"[*] Usando oferta desde caché para: {url}")
        return cached

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Use a realistic User-Agent
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print(f"[*] Accediendo a la oferta: {url}")
        
        try:
            # Go to the URL with a random delay
            await asyncio.sleep(random.uniform(1.5, 3.5))
            await page.goto(url, wait_until="networkidle")
            
            # Wait for content to load
            await page.wait_for_timeout(2000)
            
            # Basic scraping logic for common job boards (LinkedIn, InfoJobs)
            # We try to get the most relevant text content
            content = await page.evaluate("""() => {
                const selectors = [
                    '.jobs-description', '.job-details', '#job-description', 
                    '[class*="description"]', '[class*="detail"]', 'article'
                ];
                for (let selector of selectors) {
                    const el = document.querySelector(selector);
                    if (el && el.innerText.length > 200) return el.innerText;
                }
                return document.body.innerText;
            }""")
            
            title = await page.title()
            
            result = {
                "title": title,
                "content": content[:10000] # Limit content for LLM safety
            }
            save_to_cache(url, result)
            return result
            
        except Exception as e:
            print(f"[!] Error al scrapper: {e}")
            return None
        finally:
            await browser.close()

if __name__ == "__main__":
    # Test script
    import sys
    if len(sys.argv) > 1:
        result = asyncio.run(scrape_job_offer(sys.argv[1]))
        if result:
            print(f"--- Título ---\n{result['title']}\n--- Contenido ---\n{result['content'][:500]}...")
