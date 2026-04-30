# COMP3011 Coursework 2 – Search Engine Tool

## Project Overview and Purpose

This project is a Python command-line search engine that crawls https://quotes.toscrape.com/, builds an inverted index, and allows users to search for words and phrases across all crawled pages.

The crawler follows pagination until no next page exists, applying a 6-second politeness delay between requests. For each page, it strips scripts and styles before extracting text, then passes the content to the indexer.

The inverted index maps each word to the pages it appears on, storing the frequency and the position of every occurrence. Positions are stored because they allow phrase search - when the query is wrapped in quotes, the engine checks that the terms appear consecutively in the document rather than just anywhere on the page. This uses the position data directly without needing any changes to the index structure.

Search results are ranked using TF-IDF. The scoring formula is:

```
score = sum(tf * idf) for each query term
idf   = log((1 + N) / (1 + df)) + 1
```

where `tf` is the term frequency in the document, `df` is the number of documents containing the term, and `N` is the total number of documents. The `+1` smoothing prevents division by zero and reduces the weight of very rare terms, which produces more balanced rankings than standard IDF on a small corpus like this one.

When a search term is not found in the index, the engine computes the Levenshtein edit distance between the query word and every word in the index vocabulary, then suggests the closest matches. This gives users a useful path forward instead of a dead end.

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

Run the program:

```bash
python3 -m src.main
```

### Commands

Build the index (crawls the website and saves the result to `data/index.json`):

```text
> build
```

Load an existing index from file:

```text
> load
```

Print the inverted index entry for a word, showing frequency and positions per page:

```text
> print life
```

Search for pages containing all query words, ranked by TF-IDF score:

```text
> find life
> find good friends
```

Search for an exact phrase (terms must appear consecutively):

```text
> find "the world"
> find "life is"
```

If a term is not found, the engine suggests similar words:

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

Run tests with coverage:

```bash
pytest --cov=src
```

Run with verbose output to see each test name:

```bash
pytest -v
```

The test suite covers crawling (pagination, HTTP errors, text extraction), indexing (tokenisation, frequency, positions), storage (save/load roundtrip, missing file), and all search functionality including phrase search, query suggestions, multi-word intersection, edge cases, and the full CLI loop.

---

## Dependencies

The project uses the following libraries:

- `requests` - HTTP requests for the crawler
- `beautifulsoup4` - HTML parsing and text extraction
- `pytest` - test framework
- `pytest-cov` - test coverage reporting

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## Submission Notes

The generated index file is saved to `data/index.json` and is included in the submission. It can be rebuilt at any time by running the `build` command.
