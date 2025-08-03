from playwright.sync_api import sync_playwright
import os
import time

BASE_URL = "https://en.wikisource.org"

def fetch_chapter(url: str, filename: str):
    os.makedirs("data/raw_html", exist_ok=True)
    os.makedirs("data/screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=15000)
            html = page.content()
            with open(f"data/raw_html/{filename}.html", "w", encoding="utf-8") as f:
                f.write(html)
            page.screenshot(path=f"data/screenshots/{filename}.png")
            print(f"[✓] Saved: {filename}")
        except Exception as e:
            print(f"[✗] Error fetching {url}: {e}")
        finally:
            browser.close()

def get_chapter_links(index_url: str):
    chapter_links = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(index_url)

        # Get all <a> tags inside <div id="mw-content-text">
        anchors = page.locator("div#mw-content-text a")
        count = anchors.count()

        for i in range(count):
            href = anchors.nth(i).get_attribute("href")
            text = anchors.nth(i).inner_text()
            if href and "/wiki/The_Gates_of_Morning/Book_1/Chapter" in href:
                chapter_links.append(BASE_URL + href)
        browser.close()
    return chapter_links


if __name__ == "__main__":
    index_page = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1"
    print("[~] Fetching chapter links...")
    links = get_chapter_links(index_page)
    print(f"[~] Found {len(links)} chapters.")

    for idx, chapter_url in enumerate(links, start=1):
        filename = f"chapter{idx}"
        print(f"[→] Fetching: {chapter_url}")
        fetch_chapter(chapter_url, filename)
        time.sleep(1)
