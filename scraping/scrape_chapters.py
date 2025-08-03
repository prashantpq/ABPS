import os
import requests
from bs4 import BeautifulSoup

def download_chapter(url, output_dir):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        chapter_title = soup.title.string if soup.title else "chapter"

        safe_title = "".join(c for c in chapter_title if c.isalnum() or c in (" ", "_")).rstrip()
        filename = f"{safe_title}.html"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Saved: {filepath}")
        return filepath

    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def scrape_all_chapters(url_list, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    saved_paths = []
    for url in url_list:
        path = download_chapter(url, output_dir)
        if path:
            saved_paths.append(path)
    return saved_paths
