import json
import math
from pathlib import Path


DEFAULT_INDEX_PATH = Path("data/index.json")


def save_index(index: dict, file_path: Path = DEFAULT_INDEX_PATH) -> None:
    """Save the inverted index to a JSON file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(index, file, indent=2, ensure_ascii=False)


def load_index(file_path: Path = DEFAULT_INDEX_PATH) -> dict:
    """Load the inverted index from a JSON file."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"No index file found at {file_path}. Run 'build' before 'load'."
        )

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def compute_tfidf_score(index: dict, terms: list[str], url: str, total_docs: int) -> float:
    """
    Compute a smoothed TF-IDF score for a document given a set of query terms.

    Uses the formula: score = sum(tf * idf) for each term, where
    idf = log((1 + N) / (1 + df)) + 1. The smoothing (+1 to numerator
    and denominator) prevents division by zero and reduces the impact
    of very rare terms, following standard IR practice.

    Complexity: O(T) where T is the number of query terms.
    """
    score = 0.0

    for term in terms:
        tf = index[term][url]["frequency"]
        df = len(index[term])

        idf = math.log((1 + total_docs) / (1 + df)) + 1

        score += tf * idf

    return score