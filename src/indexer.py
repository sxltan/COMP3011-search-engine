import re
from collections import defaultdict


def tokenize(text: str) -> list[str]:
    """
    Convert text into lowercase word tokens.

    The search is case-insensitive, so words like 'Good' and 'good'
    are treated as the same word. Punctuation is ignored by matching
    only word characters.

    Complexity: O(n) where n is the length of the input text.
    """
    return re.findall(r"\b\w+\b", text.lower())


def build_index(pages: list[dict[str, str]]) -> dict[str, dict[str, dict[str, list[int] | int]]]:
    """
    Build an inverted index from crawled pages.

    Each word maps to the set of pages it appears in, storing its
    frequency and the positions of each occurrence. Position data
    enables phrase search and proximity analysis.

    Structure:
    {
        word: {
            url: {
                "frequency": int,
                "positions": [int, int, ...]
            }
        }
    }

    Complexity: O(P * W) where P is the number of pages and W is the
    average number of words per page.
    """
    index = defaultdict(lambda: defaultdict(lambda: {
        "frequency": 0,
        "positions": []
    }))

    for page in pages:
        url = page["url"]
        words = tokenize(page["text"])

        for position, word in enumerate(words):
            index[word][url]["frequency"] += 1
            index[word][url]["positions"].append(position)

    return {
        word: dict(page_data)
        for word, page_data in index.items()
    }