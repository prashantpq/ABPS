import os
from pathlib import Path
from typing import Dict, List, Tuple

# Directory where your cleaned text data is stored
CLEANED_DATA_DIR = Path("data/cleaned")

def load_chapter_texts() -> Dict[str, str]:
    """
    Loads all cleaned chapter text files.

    Returns:
        dict: Dictionary of {filename (without .txt): content}
    """
    if not CLEANED_DATA_DIR.exists():
        raise FileNotFoundError(f"[!] Cleaned data folder not found at {CLEANED_DATA_DIR}")

    data = {}
    for file in CLEANED_DATA_DIR.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            data[file.stem] = f.read()
    return data

def score_chapter(text: str) -> float:
    """
    Dummy scoring function: returns a score between 0 and 1 based on length.
    """
    score = min(1.0, len(text) / 1000)
    return round(score, 3)

def evaluate_all_chapters(chapter_data):
    if not chapter_data:
        print("[!] No chapter data provided. Please check input.\n")
        return None

    print(f"[~] Received {len(chapter_data)} chapters for evaluation...\n")

    results = []

    for idx, chapter in enumerate(chapter_data):
        print(f"[*] Evaluating chapter {idx + 1}: {chapter[:60]}...")  # preview
        try:
            score = score_chapter(chapter)
            results.append((chapter, score))
        except Exception as e:
            print(f"[x] Error evaluating chapter {idx + 1}: {e}")
            continue

    if not results:
        print("[!] No chapters were successfully evaluated.\n")
        return None

    avg_score = round(sum(score for _, score in results) / len(results), 4)

    print(f"\n[✓] Evaluation complete. Average Score: {avg_score}\n")

    return {
        "average_score": avg_score,
        "chapter_scores": results
    }


# If run directly
if __name__ == "__main__":
    try:
        data = load_chapter_texts()
        summary = evaluate_all_chapters(data)
        print("\n--- Evaluation Summary ---")
        print(summary)
    except FileNotFoundError as e:
        print(e)
