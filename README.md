# COMP3011 Coursework 2 – Search Engine Tool

## Project Overview and Purpose

This project is a Python command-line search engine that crawls the website https://quotes.toscrape.com/, builds an inverted index, and allows users to search for one or more words (all terms must appear in results).

The system retrieves all pages, extracts text content, and stores word statistics such as frequency and position. Users can then query the index using different commands to retrieve relevant pages. Search results are ranked using a smoothed TF-IDF scoring approach. The crawler respects a 6-second politeness delay between requests.

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

Build the index (crawls the website and saves data):

```text
> build
```

Load an existing index:

```text
> load
```

Print the inverted index for a word:

```text
> print life
```

Search for pages containing one or more words. For multi-word searches, all terms must appear:

```text
> find life
> find good friends
```

Handle missing or invalid input:

```text
> find nonsenseword
> find
> print
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

The tests cover crawling, indexing, storage, and search functionality, including edge cases such as missing terms, empty queries, pagination, and failure handling.

---

## Dependencies

The project uses the following libraries:

- requests
- beautifulsoup4
- pytest
- pytest-cov

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## Submission Notes

The generated index file is saved to:

```text
data/index.json
```

This file is created using the build command and is included in the final submission as required.