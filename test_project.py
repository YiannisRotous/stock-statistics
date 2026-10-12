import pytest
import statistics
import yfinance as yf
from project import extract_ticker, compute_statistics, is_valid_url, fetch_last_month_prices

# -----------------------------
# Test extract_ticker
# -----------------------------

def test_extract_ticker_normal():
    assert extract_ticker("https://finance.yahoo.com/quote/AAPL/") == "AAPL"

def test_extract_ticker_encoded():
    assert extract_ticker("https://finance.yahoo.com/quote/%5EVIX/") == "^VIX"

def test_extract_ticker_invalid():
    with pytest.raises(ValueError):
        extract_ticker("https://google.com/not-a-stock")


# -----------------------------
# Test compute_statistics
# -----------------------------

def test_compute_statistics_basic():
    prices = [10, 20, 30]
    stats = compute_statistics(prices)

    assert stats["mean"] == statistics.mean(prices)
    assert stats["median"] == statistics.median(prices)
    assert stats["stdev"] == statistics.stdev(prices)
    assert stats["min"] == min(prices)
    assert stats["max"] == max(prices)

def test_compute_statistics_single_value():
    prices = [42]
    stats = compute_statistics(prices)

    assert stats["mean"] == 42
    assert stats["median"] == 42
    assert stats["stdev"] == 0
    assert stats["min"] == 42
    assert stats["max"] == 42


# -----------------------------
# Test is_valid_url (mock requests)
# -----------------------------

import requests

def test_is_valid_url_success(monkeypatch):
    class MockResponse:
        status_code = 200

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    assert is_valid_url("https://finance.yahoo.com/quote/AAPL/") is True


def test_is_valid_url_failure(monkeypatch):
    def mock_get(*args, **kwargs):
        raise Exception("Network error")

    monkeypatch.setattr(requests, "get", mock_get)
    assert is_valid_url("https://finance.yahoo.com/quote/AAPL/") is False


# -----------------------------
# Test fetch_last_month_prices (mock yfinance)
# -----------------------------

def test_fetch_last_month_prices(monkeypatch):
    class FakeTicker:
        def history(self, period):
            return {"Close": [100, 101, 102]}

    monkeypatch.setattr(yf, "Ticker", lambda ticker: FakeTicker())
    prices = fetch_last_month_prices("AAPL")

    assert prices == [100, 101, 102]


def test_fetch_last_month_prices_empty(monkeypatch):
    class FakeTicker:
        def history(self, period):
            class EmptyData:
                empty = True
            return EmptyData()

    monkeypatch.setattr(yf, "Ticker", lambda ticker: FakeTicker())

    with pytest.raises(ValueError):
        fetch_last_month_prices("AAPL")
