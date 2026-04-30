"""
Benchmark script to verify the time complexity of key algorithms.

Run with: python3 benchmark.py

Measures how build_index and find_pages scale with input size,
confirming the O(P * W) and O(T * U) complexity documented in the
function docstrings.
"""

import contextlib
import io
import time

from src.indexer import build_index
from src.main import find_pages


def make_pages(n: int, words_per_page: int = 200) -> list[dict[str, str]]:
    """Generate n synthetic pages with a fixed number of words each."""
    return [
        {
            "url": f"https://example.com/page/{i}",
            "text": " ".join(f"word{j}" for j in range(words_per_page)),
        }
        for i in range(n)
    ]


def benchmark_build_index() -> None:
    """
    Time build_index at increasing page counts.

    Expects roughly linear growth, confirming O(P * W).
    """
    print("build_index — O(P * W) where P = pages, W = words per page")
    print(f"  {'Pages':>6}  {'Time (s)':>10}")
    print("  " + "-" * 20)

    for n in [10, 50, 100, 200, 500]:
        pages = make_pages(n)
        start = time.perf_counter()
        build_index(pages)
        elapsed = time.perf_counter() - start
        print(f"  {n:>6}  {elapsed:>10.4f}")

    print()


def benchmark_find_pages() -> None:
    """
    Time find_pages at increasing index sizes.

    Expects roughly linear growth with vocabulary size, confirming O(T * U).
    """
    print("find_pages — O(T * U) where T = query terms, U = URLs per term")
    print(f"  {'Pages':>6}  {'Time (s)':>10}")
    print("  " + "-" * 20)

    for n in [10, 50, 100, 200, 500]:
        pages = make_pages(n)
        index = build_index(pages)

        start = time.perf_counter()
        with contextlib.redirect_stdout(io.StringIO()):
            find_pages(index, "word0 word1 word2")
        elapsed = time.perf_counter() - start

        print(f"  {n:>6}  {elapsed:>10.6f}")

    print()


if __name__ == "__main__":
    benchmark_build_index()
    benchmark_find_pages()
