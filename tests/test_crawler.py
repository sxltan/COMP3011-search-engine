import requests

from src.crawler import crawl_site, extract_page_text, fetch_page, get_next_page_url


def test_extract_page_text_removes_script_and_style():
    html = """
    <html>
        <head>
            <style>.hidden { color: red; }</style>
            <script>alert("hello");</script>
        </head>
        <body>
            <p>Hello world</p>
        </body>
    </html>
    """

    text = extract_page_text(html)

    assert "Hello world" in text
    assert "alert" not in text
    assert "hidden" not in text


def test_get_next_page_url_returns_absolute_url():
    html = '<li class="next"><a href="/page/2/">Next</a></li>'

    next_url = get_next_page_url(html, "https://quotes.toscrape.com/")

    assert next_url == "https://quotes.toscrape.com/page/2/"


def test_get_next_page_url_returns_none_when_missing():
    html = "<html><body>No next page</body></html>"

    next_url = get_next_page_url(html, "https://quotes.toscrape.com/page/10/")

    assert next_url is None


def test_fetch_page_returns_html_on_success(monkeypatch):
    class MockResponse:
        text = "<html>Success</html>"

        def raise_for_status(self):
            return None

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    result = fetch_page("https://example.com")

    assert result == "<html>Success</html>"


def test_fetch_page_handles_http_error(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            raise requests.HTTPError("404 error")

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    result = fetch_page("https://example.com")

    assert result is None


def test_crawl_site_follows_pagination(monkeypatch):
    first_page = """
    <html>
        <body>
            <p>First page text</p>
            <li class="next"><a href="/page/2/">Next</a></li>
        </body>
    </html>
    """

    second_page = """
    <html>
        <body>
            <p>Second page text</p>
        </body>
    </html>
    """

    pages = {
        "https://quotes.toscrape.com/": first_page,
        "https://quotes.toscrape.com/page/2/": second_page,
    }

    def fake_fetch_page(url):
        return pages[url]

    monkeypatch.setattr("src.crawler.fetch_page", fake_fetch_page)

    crawled_pages = crawl_site(delay=0)

    assert len(crawled_pages) == 2
    assert crawled_pages[0]["url"] == "https://quotes.toscrape.com/"
    assert crawled_pages[1]["url"] == "https://quotes.toscrape.com/page/2/"
    assert "First page text" in crawled_pages[0]["text"]
    assert "Second page text" in crawled_pages[1]["text"]


def test_crawl_site_stops_when_fetch_fails(monkeypatch):
    def fake_fetch_page(url):
        return None

    monkeypatch.setattr("src.crawler.fetch_page", fake_fetch_page)

    crawled_pages = crawl_site(delay=0)

    assert crawled_pages == []