# scraping/rl_scrape_evaluator.py
import os
from bs4 import BeautifulSoup

def evaluate_html_quality(html_path):
    try:
        with open(html_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            
            text = soup.get_text(strip=True)
            if not text:
                return "No text found", 0
            elif len(text) < 500:
                return "Too little content", 1
            elif len(text) > 10000:
                return "Content too long", 2
            else:
                return "Good content", 3
    except Exception as e:
        return f"Error: {str(e)}", 0

def evaluate_all_chapters(data_folder):
    results = []
    html_folder = os.path.join(data_folder, "raw_html")
    if not os.path.exists(html_folder):
        print("No raw_html directory found")
        return results

    for filename in os.listdir(html_folder):
        if filename.endswith(".html"):
            filepath = os.path.join(html_folder, filename)
            message, score = evaluate_html_quality(filepath)
            results.append((filename, score))
            print(f"{filename}: {message} (Score: {score})")

    if not results:
        print("No HTML files found for evaluation")
        return results

    avg_score = round(sum(score for _, score in results) / len(results), 4)
    print(f"\nAverage quality score: {avg_score}\n")
    return results
