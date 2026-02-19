"""Tests for RSS feed fetching and parsing."""
import sys
from pathlib import Path

import pytest
from unittest.mock import Mock, patch, MagicMock
from vfinance_news.fetch_news import fetch_market_data, fetch_rss, _get_best_feed_url, get_large_portfolio_news
from vfinance_news.utils import clamp_timeout, compute_deadline


@pytest.fixture
def sample_rss_content():
    """Load sample RSS fixture."""
    fixture_path = Path(__file__).parent / "fixtures" / "sample_rss.xml"
    return fixture_path.read_bytes()


def test_fetch_rss_success(sample_rss_content):
    """Test successful RSS fetch and parse."""
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = sample_rss_content
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        articles = fetch_rss("https://example.com/feed.xml", timeout=7)
        
        assert len(articles) == 2
        assert articles[0]["title"] == "Apple Stock Rises 5%"
        assert articles[1]["title"] == "Tesla Announces New Model"
        assert "apple-rises" in articles[0]["link"]
        assert mock_urlopen.call_args.kwargs["timeout"] == 7


def test_fetch_rss_network_error():
    """Test RSS fetch handles network errors."""
    with patch("urllib.request.urlopen", side_effect=Exception("Network error")):
        articles = fetch_rss("https://example.com/feed.xml")
        assert articles == []


def test_get_best_feed_url_priority():
    """Test feed URL selection prioritizes 'top' key."""
    source = {
        "name": "Test Source",
        "homepage": "https://example.com",
        "top": "https://example.com/top.xml",
        "markets": "https://example.com/markets.xml"
    }
    
    url = _get_best_feed_url(source)
    assert url == "https://example.com/top.xml"


def test_get_best_feed_url_fallback():
    """Test feed URL falls back to other http URLs when priority keys missing."""
    source = {
        "name": "Test Source",
        "feed": "https://example.com/feed.xml"
    }
    
    url = _get_best_feed_url(source)
    assert url == "https://example.com/feed.xml"


def test_get_best_feed_url_none_if_no_urls():
    """Test returns None when no valid URLs found."""
    source = {
        "name": "Test Source",
        "enabled": True,
        "note": "No URLs here"
    }
    
    url = _get_best_feed_url(source)
    assert url is None


def test_get_best_feed_url_skips_non_urls():
    """Test skips non-URL values."""
    source = {
        "name": "Test Source",
        "enabled": True,
        "count": 5,
        "rss": "https://example.com/rss.xml"
    }
    
    url = _get_best_feed_url(source)
    assert url == "https://example.com/rss.xml"


def test_clamp_timeout_respects_deadline(monkeypatch):
    start = 100.0
    monkeypatch.setattr("vfinance_news.utils.time.monotonic", lambda: start)
    deadline = compute_deadline(5)
    monkeypatch.setattr("vfinance_news.utils.time.monotonic", lambda: 103.0)

    assert clamp_timeout(30, deadline) == 2


def test_clamp_timeout_deadline_exceeded(monkeypatch):
    start = 200.0
    monkeypatch.setattr("vfinance_news.utils.time.monotonic", lambda: start)
    deadline = compute_deadline(1)
    monkeypatch.setattr("vfinance_news.utils.time.monotonic", lambda: 205.0)

    with pytest.raises(TimeoutError):
        clamp_timeout(30, deadline)


def test_fetch_market_data_empty_symbols_returns_empty():
    assert fetch_market_data([]) == {}


def test_fetch_market_data_uses_yfinance_only(monkeypatch):
    expected = {
        "AAPL": {"price": 123.45, "change_percent": 1.0, "prev_close": 122.0, "symbol": "AAPL"},
        "MSFT": {"price": 321.0, "change_percent": -0.5, "prev_close": 322.6, "symbol": "MSFT"},
    }
    monkeypatch.setattr(
        "vfinance_news.fetch_news._fetch_via_yfinance",
        lambda symbols, timeout, deadline: expected if symbols == ["AAPL", "MSFT"] and timeout == 42 and deadline == 99.0 else {},
    )

    result = fetch_market_data(["AAPL", "MSFT"], timeout=42, deadline=99.0, allow_price_fallback=True)
    assert result == expected


def test_get_large_portfolio_news_handles_none_change(monkeypatch):
    monkeypatch.setattr("vfinance_news.fetch_news.get_portfolio_symbols", lambda: ["AAA", "BBB", "CCC"])
    monkeypatch.setattr(
        "vfinance_news.fetch_news._fetch_via_yfinance",
        lambda *_a, **_k: {
            "AAA": {"change_percent": None, "price": 110.0, "prev_close": 100.0},
            "BBB": {"change_percent": -1.5, "price": 50.0},
            "CCC": {"change_percent": 2.0, "price": 20.0},
        },
    )
    monkeypatch.setattr("vfinance_news.fetch_news.fetch_market_data", lambda *_a, **_k: {})
    monkeypatch.setattr("vfinance_news.fetch_news.fetch_ticker_news", lambda *_a, **_k: [])

    result = get_large_portfolio_news(limit=1, portfolio_meta={"AAA": {"name": "Alpha"}})

    assert "stocks" in result
    assert set(result["stocks"].keys()) == {"AAA", "BBB", "CCC"}


def test_get_large_portfolio_news_respects_top_movers_count(monkeypatch):
    monkeypatch.setattr("vfinance_news.fetch_news.get_portfolio_symbols", lambda: ["AAA", "BBB", "CCC", "DDD"])
    monkeypatch.setattr(
        "vfinance_news.fetch_news._fetch_via_yfinance",
        lambda *_a, **_k: {
            "AAA": {"change_percent": 5.0, "price": 10.0},
            "BBB": {"change_percent": -4.0, "price": 20.0},
            "CCC": {"change_percent": 3.0, "price": 30.0},
            "DDD": {"change_percent": -2.0, "price": 40.0},
        },
    )
    monkeypatch.setattr("vfinance_news.fetch_news.fetch_market_data", lambda *_a, **_k: {})
    monkeypatch.setattr("vfinance_news.fetch_news.fetch_ticker_news", lambda *_a, **_k: [])

    result = get_large_portfolio_news(limit=1, top_movers_count=2, portfolio_meta={})

    assert result["meta"]["top_movers_count"] == 2
    assert len(result["stocks"]) == 2
