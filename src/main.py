from src.crawler import crawl_site
from src.indexer import build_index, tokenize
from src.search import compute_tfidf_score, load_index, save_index


def print_help() -> None:
    """Show available commands."""
    print("Commands:")
    print("  build              Crawl website, build index, and save it")
    print("  load               Load index from file")
    print("  print <word>       Print index entry for a word")
    print("  find <query>       Find pages containing all query words")
    print("  help               Show this help message")
    print("  exit               Quit the program")


def print_word(index: dict, word: str) -> None:
    """Print the inverted index entry for one word."""
    terms = tokenize(word)

    if not terms:
        print("Please provide a valid word.")
        return

    word = terms[0]

    if word not in index:
        print(f"No results found for '{word}'.")
        return

    print(f"Inverted index for '{word}':")
    for url, stats in index[word].items():
        print(f"- {url}")
        print(f"  frequency: {stats['frequency']}")
        print(f"  positions: {stats['positions']}")


def get_total_documents(index: dict) -> int:
    """
    Count the number of unique pages stored in the index.

    Complexity: O(V * U) where V is the vocabulary size and U is the
    average number of URLs per word.
    """
    return len({url for word_data in index.values() for url in word_data})


def has_consecutive_positions(index: dict, terms: list[str], url: str) -> bool:
    """
    Check whether the given terms appear consecutively in a document.

    Used for phrase search to verify that query words appear in sequence,
    not just anywhere on the same page. Converts each term's position list
    to a set for O(1) lookup per offset check.

    Complexity: O(T * F) where T is the number of terms and F is the
    frequency of the first term in the document.
    """
    if len(terms) == 1:
        return True

    position_sets = [
        set(index[term][url]["positions"])
        for term in terms
    ]

    for start in position_sets[0]:
        if all(start + offset in position_sets[offset] for offset in range(1, len(terms))):
            return True

    return False


def find_pages(index: dict, query: str) -> None:
    """
    Find pages that contain all query words and rank them with TF-IDF.

    If the query is wrapped in double quotes, phrase mode is used:
    results are filtered to pages where the terms appear consecutively,
    using the position data stored in the index.

    Complexity: O(T * U) where T is the number of query terms and U is
    the average number of URLs per term.
    """
    phrase_mode = query.startswith('"') and query.endswith('"') and len(query) > 2
    if phrase_mode:
        query = query[1:-1].strip()

    terms = tokenize(query)

    if not terms:
        print("Please provide at least one search term.")
        return

    missing_terms = [term for term in terms if term not in index]

    if missing_terms:
        print(f"No results found. Missing term(s): {', '.join(missing_terms)}")
        return

    matching_urls = set(index[terms[0]].keys())

    for term in terms[1:]:
        matching_urls = matching_urls.intersection(index[term].keys())

    if phrase_mode:
        matching_urls = {
            url for url in matching_urls
            if has_consecutive_positions(index, terms, url)
        }

    if not matching_urls:
        print("No pages contain all query terms.")
        return

    total_docs = get_total_documents(index)

    scored_results = [
        (url, compute_tfidf_score(index, terms, url, total_docs))
        for url in matching_urls
    ]

    scored_results.sort(key=lambda result: result[1], reverse=True)

    print(f"Results for '{query}':")
    for url, score in scored_results:
        print(f"- {url} (score: {score:.3f})")


def run_shell() -> None:
    """Run the command-line search tool."""
    index = None

    print("COMP3011 Search Engine Tool")
    print("Type 'help' to see available commands.")
    print("Note: 'build' may take about one minute due to the politeness delay.")

    while True:
        command_line = input("> ").strip()

        if not command_line:
            print("Please enter a command.")
            continue

        parts = command_line.split(maxsplit=1)
        command = parts[0].lower()
        argument = parts[1] if len(parts) > 1 else ""

        if command == "exit":
            print("Goodbye.")
            break

        if command == "help":
            print_help()

        elif command == "build":
            print("Crawling website. This may take about one minute due to politeness delay...")
            pages = crawl_site()
            index = build_index(pages)
            save_index(index)
            print(f"Index built and saved. Crawled {len(pages)} pages and indexed {len(index)} words.")

        elif command == "load":
            try:
                index = load_index()
                print(f"Index loaded. Indexed words: {len(index)}")
            except FileNotFoundError as error:
                print(error)

        elif command == "print":
            if index is None:
                print("No index loaded. Run 'build' or 'load' first.")
            elif not argument:
                print("Usage: print <word>")
            else:
                print_word(index, argument)

        elif command == "find":
            if index is None:
                print("No index loaded. Run 'build' or 'load' first.")
            elif not argument:
                print("Usage: find <query>")
            else:
                find_pages(index, argument)

        else:
            print(f"Unknown command: {command}")
            print("Type 'help' to see available commands.")


if __name__ == "__main__":
    run_shell()