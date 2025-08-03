from playwright.sync_api import sync_playwright
import os
import time

BASE_URL = "https://en.wikisource.org"
RAW_HTML_DIR = "data/raw_html"
SCREENSHOT_DIR = "data/screenshots"

# Create necessary directories
os.makedirs(RAW_HTML_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def fetch_chapter(url: str, filename: str):
    """
    Fetches HTML content and screenshot of a chapter page.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            print(f"[→] Navigating to: {url}")
            page.goto(url, timeout=20000)
            html = page.content()

            # Save HTML
            html_path = os.path.join(RAW_HTML_DIR, f"{filename}.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)

            # Save screenshot
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"{filename}.png")
            page.screenshot(path=screenshot_path, full_page=True)

            print(f"[✓] Saved {filename}.html and {filename}.png")
        except Exception as e:
            print(f"[✗] Failed to fetch {url}: {e}")
        finally:
            browser.close()

def get_chapter_links(index_url: str):
    """
    Returns a list of absolute chapter URLs from the index page.
    """
    chapter_links = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"[~] Loading index page: {index_url}")
        try:
            page.goto(index_url, timeout=15000)
            anchors = page.locator("div#mw-content-text a")
            count = anchors.count()
            print(f"[~] Found {count} anchor tags.")

            for i in range(count):
                try:
                    href = anchors.nth(i).get_attribute("href")
                    if href and "/wiki/The_Gates_of_Morning/Book_1/Chapter" in href:
                        full_url = BASE_URL + href
                        if full_url not in chapter_links:
                            chapter_links.append(full_url)
                except Exception:
                    continue
        except Exception as e:
            print(f"[✗] Error loading index page: {e}")
        finally:
            browser.close()
    return chapter_links

if __name__ == "__main__":
    index_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1"
    print("[~] Starting scraper...")

    chapter_urls = get_chapter_links(index_url)
    print(f"[✓] Found {len(chapter_urls)} chapter links.\n")

    for idx, url in enumerate(chapter_urls, 1):
        filename = f"chapter{idx:02d}"
        fetch_chapter(url, filename)
        time.sleep(1)  # Politeness delay

    print("\n[✓] Scraping completed.")
