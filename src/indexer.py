import re
from collections import defaultdict


def tokenize(text: str) -> list[str]:
    """
    Convert text into lowercase words.

    The search is case-insensitive, so words like 'Good' and 'good'
    are treated as the same word.
    """
    return re.findall(r"\b\w+\b", text.lower())


def build_index(pages: list[dict[str, str]]) -> dict[str, dict[str, dict[str, list[int] | int]]]:
    """
    Build an inverted index from crawled pages.

    Structure:
    {
        word: {
            url: {
                "frequency": int,
                "positions": [int, int, ...]
            }
        }
    }
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