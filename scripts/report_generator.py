import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraping.scrape_chapters import scrape_all_chapters
from scraping.rl_scrape_evaluator import evaluate_all_chapters  # If used

def generate_report():
    url_list = [
    # Classic public domain physics books - Project Gutenberg
    "https://www.gutenberg.org/files/40175/40175-h/40175-h.htm",  # *Physics* (Willis E. Tower et al.)
    "https://www.gutenberg.org/files/20417/20417-h/20417-h.htm",  # The Concept of Nature by A.N. Whitehead
    "https://www.gutenberg.org/files/1225/1225-h/1225-h.htm",    # *Faraday as a Discoverer* (John Tyndall)
    "https://www.gutenberg.org/files/69022/69022-h/69022-h.htm"   # *Worlds in the Making* (Svante Arrhenius)
    ]
    output_dir = os.path.join(os.path.dirname(__file__), "../data/raw_html")

    print("Starting scraping...")
    scraped_files = scrape_all_chapters(url_list, output_dir)

    print("\nEvaluating content quality...")
    evaluation = evaluate_all_chapters(os.path.join(os.path.dirname(__file__), "../data"))

    print("\n--- Report Summary ---")
    print(f"Total chapters scraped: {len(scraped_files)}")
    print(f"Total evaluated: {len(evaluation)}")

if __name__ == "__main__":
    generate_report()
