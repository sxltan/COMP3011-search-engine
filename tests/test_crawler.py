from src.crawler import extract_page_text, get_next_page_url


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