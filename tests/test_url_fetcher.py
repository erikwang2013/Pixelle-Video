import pytest


def test_url_validation():
    """URLFetcher should validate URLs correctly"""
    from pixelle_video.services.url_fetcher import URLFetcher
    fetcher = URLFetcher()
    assert fetcher._is_valid_url("https://example.com/article") is True
    assert fetcher._is_valid_url("http://example.com") is True
    assert fetcher._is_valid_url("http://localhost:8080/path") is True
    assert fetcher._is_valid_url("not-a-url") is False
    assert fetcher._is_valid_url("ftp://invalid.com") is False
    assert fetcher._is_valid_url("") is False


def test_extract_article_text():
    """Should extract text from HTML, removing script/style tags"""
    from pixelle_video.services.url_fetcher import URLFetcher
    fetcher = URLFetcher()
    html = """
    <html><head><title>Test Article</title></head>
    <body>
    <script>alert(1)</script>
    <style>.x{color:red}</style>
    <article><p>This is the article content.</p><p>Second paragraph.</p></article>
    </body></html>
    """
    text = fetcher.extract_article_text(html)
    assert "article content" in text
    assert "Second paragraph" in text
    assert "alert" not in text
    assert ".x" not in text


def test_extract_title():
    """Should extract title from HTML"""
    from pixelle_video.services.url_fetcher import URLFetcher
    fetcher = URLFetcher()
    html_with_title = "<html><head><title>My Page</title></head><body></body></html>"
    assert fetcher._extract_title(html_with_title) == "My Page"

    html_with_h1 = "<html><head></head><body><h1>Heading</h1></body></html>"
    assert fetcher._extract_title(html_with_h1) == "Heading"

    html_no_title = "<html><body></body></html>"
    assert fetcher._extract_title(html_no_title) == "Untitled"
