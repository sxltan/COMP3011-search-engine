# COMP3011 Coursework 2 – Search Engine Tool

## Project Overview and Purpose

This project is a Python command-line search engine that crawls https://quotes.toscrape.com/, builds an inverted index, and lets you search for words and phrases across every crawled page.

The crawler follows pagination until there is no "next" link, waits **6 seconds** between requests (except before the first fetch), strips `<script>` and `<style>` content, then passes plain text to the indexer.

The inverted index maps each word to the URLs where it appears, storing **frequency** and **token positions** (each word's index in the token sequence after tokenisation). **Phrase search** is triggered by double quotes: terms must appear at **consecutive** positions in that sequence (each step +1), not only somewhere on the same page.

Queries are ranked with **smoothed TF-IDF**. Per query term in a document:

```
score = sum(tf * idf) over query terms
idf   = log((1 + N) / (1 + df)) + 1
```

Here **`tf`** is raw term frequency in that document, **`df`** is how many indexed documents contain the term, and **`N`** is the total number of distinct indexed documents (unique URLs in the index). Adding **`1`** above and below avoids degenerate behaviour when **`df`** is very small and **pulls extreme IDF values toward the middle**, which stabilises ranking on a small corpus compared with unsmoothed **`log(N / df)`** IDF.

If a typed word is missing from the index, the tool compares it to the vocabulary with **Levenshtein edit distance**, keeps matches within distance **2**, and prints up to **three** "Did you mean?" suggestions (closest first).

---

## Installation and Setup

1. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage Examples

Run the program from the repository root:

```bash
python3 -m src.main
```

### Commands

Build the index (crawls the site and writes `data/index.json`):

```text
> build
```

Load a saved index:

```text
> load
```

Print one word’s postings (frequency and positions per URL):

```text
> print life
```

Conjunctive search: **every** word must occur somewhere on the page; results are sorted by TF-IDF score.

```text
> find life
> find good friends
```

Phrase search (tokens must be consecutive in the indexed sequence):

```text
> find "the world"
> find "life is"
```

Unknown token with nearby vocabulary matches:

```text
> find freinds
No results found. Missing term(s): freinds
  Did you mean: friends?
```

---

## Testing Instructions

Run all tests:

```bash
pytest
```

With coverage over `src/`:

```bash
pytest --cov=src
```

Verbose listing:

```bash
pytest -v
```

### Testing strategy

Tests avoid calling the live website: crawler pagination and HTTP failures use **pytest `monkeypatch`** on `requests.get` or `fetch_page`. Save/load tests use **`tmp_path`** so nothing writes outside the temp directory. The interactive shell is driven by mocking **`builtins.input`** with fixed command sequences. One integration-style test builds an index, writes JSON with **`save_index`**, reloads with **`load_index`**, then runs **`find_pages`**—still without network I/O.

**Optional tooling:** `benchmark.py` times `build_index` and `find_pages` on synthetic pages (run `python3 benchmark.py`). **GitHub Actions** (`.github/workflows/tests.yml`) runs the same pytest suite on pushes and pull requests.

---

## Dependencies

Runtime:

- `requests` — HTTP client for the crawler  
- `beautifulsoup4` — HTML parsing and visible-text extraction  

Development:

- `pytest` — test runner  
- `pytest-cov` — coverage reporting  

Install everything listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Submission Notes

The committed artefact is **`data/index.json`**. Regenerate it anytime with **`build`** after activating the virtual environment and installing dependencies.
