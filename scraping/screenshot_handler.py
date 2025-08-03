import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

SCREENSHOT_DIR = Path("data/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


async def capture_screenshot(url: str, filename: str = None, full_page: bool = True):
    """
    Captures a screenshot of the given URL using Playwright.

    Args:
        url (str): Web page URL to capture.
        filename (str, optional): Name for the screenshot file. Defaults to slugified URL.
        full_page (bool, optional): Capture entire page or just viewport.

    Returns:
        str: Path to saved screenshot image.
    """
    filename = filename or url.replace("://", "_").replace("/", "_") + ".png"
    save_path = SCREENSHOT_DIR / filename

    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(url, timeout=15000)
            await page.screenshot(path=str(save_path), full_page=full_page)

            await browser.close()
            print(f"[✔] Screenshot saved: {save_path}")
            return str(save_path)

    except Exception as e:
        print(f"[✖] Failed to capture screenshot for {url}: {e}")
        return None


async def batch_capture(urls: list[str]):
    """
    Captures screenshots for a list of URLs.

    Args:
        urls (list): List of URLs to capture.
    """
    for url in urls:
        await capture_screenshot(url)


# If run as a script
if __name__ == "__main__":
    import sys

    urls = sys.argv[1:]
    if not urls:
        print("Usage: python screenshot_handler.py <url1> <url2> ...")
    else:
        asyncio.run(batch_capture(urls))
