import os
import sys
from datetime import datetime

# Allow importing from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraping.scrape_chapters import fetch_chapter
from scraping.rl_scrape_evaluator import evaluate_all_chapters, load_chapter_texts
from scraping.screenshot_handler import capture_screenshot  # If implemented

# Set the URL and filename (adjust URL to target site)
SCRAPE_URL = "https://www.abps.org.in/abps-annual-reports/"
SAVE_FILENAME = "abps_chapters_raw.txt"

def generate_report():
    print("📥 Starting data scraping...")
    fetch_chapter(SCRAPE_URL, SAVE_FILENAME)  # This saves HTML/screenshot

    print("📖 Loading chapter texts...")
    try:
        data = load_chapter_texts()
    except FileNotFoundError as e:
        print(f"[✗] {e}")
        return

    print("🧪 Evaluating scraped data...")
    evaluation = evaluate_all_chapters(data)

    print("📸 Capturing screenshot of results...")
    try:
        capture_screenshot()
    except:
        print("[!] Screenshot capture skipped or failed.")

    print("📝 Preparing report...")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"report_{timestamp}.txt"

    with open(report_filename, 'w') as report_file:
        report_file.write("📄 Scrape Report\n")
        report_file.write("====================\n")
        report_file.write(f"🕒 Timestamp: {timestamp}\n\n")

        report_file.write("📊 Evaluation Summary:\n")
        for chapter, score in evaluation:
            report_file.write(f"- {chapter}: {score}\n")

        report_file.write("\n🧾 Sample Data:\n")
        for i, (chapter, content) in enumerate(data.items()):
            if i >= 3:
                break
            report_file.write(f"\n--- {chapter} ---\n")
            report_file.write(content[:500] + "...\n")  # Preview

    print(f"✅ Report saved as: {report_filename}")

if __name__ == "__main__":
    generate_report()
