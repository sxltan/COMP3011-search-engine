import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com/"
DEFAULT_DELAY = 6


def fetch_page(url: str) -> str | None:
    """Fetch a page and return its HTML, or None if the request fails."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as error:
        print(f"Error fetching {url}: {error}")
        return None


def extract_page_text(html: str) -> str:
    """Extract readable text from a page."""
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    return soup.get_text(separator=" ", strip=True)


def get_next_page_url(html: str, current_url: str) -> str | None:
    """Find the next page link, if one exists."""
    soup = BeautifulSoup(html, "html.parser")
    next_link = soup.select_one("li.next a")

    if next_link is None:
        return None

    return urljoin(current_url, next_link.get("href"))


def crawl_site(start_url: str = BASE_URL, delay: int = DEFAULT_DELAY) -> list[dict[str, str]]:
    """
    Crawl the quotes website and return a list of pages.

    Each page is stored as:
    {
        "url": page URL,
        "text": extracted page text
    }
    """
    pages = []
    current_url = start_url
    first_request = True

    while current_url:
        if not first_request:
            time.sleep(delay)

        html = fetch_page(current_url)

        if html is None:
            break

        pages.append({
            "url": current_url,
            "text": extract_page_text(html),
        })

        current_url = get_next_page_url(html, current_url)
        first_request = False

    return pages