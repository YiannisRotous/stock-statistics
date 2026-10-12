import requests
from urllib.parse import unquote
import yfinance as yf
import statistics


def main():
    print("Enter stock URLs (type 'done' to finish):")

    urls = []
    while True:
        url = input("URL: ").strip()

        # Stop when user types "done"
        if url.lower() == "done":
            break

        if url == "":
            print("Please enter a URL.")
            continue

        if not is_valid_url(url):
            print("Invalid or unreachable URL. Please try again.")
            continue

        try:
            ticker = extract_ticker(url)
        except ValueError:
            print("URL format not recognized. Please enter a valid stock URL.")
            continue

        urls.append(url)
        print("URL accepted.")

    if not urls:
        sys.exit("No valid URLs provided.")

    for url in urls:
        ticker = extract_ticker(url)
        prices = fetch_last_month_prices(ticker)
        stats = compute_statistics(prices)
        print_summary(ticker, stats)

def is_valid_url(url):
    """
    Check if the URL is reachable and correctly formatted.
    Uses a browser-like User-Agent to avoid Yahoo blocking the request.
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def extract_ticker(url):
    """
    Extract ticker from any Yahoo Finance URL.
    Handles encoded characters, trailing slashes, and query parameters.
    """
    if "/quote/" not in url:
        raise ValueError("Not a valid Yahoo Finance stock URL")

    try:
        # Take the part after /quote/
        part = url.split("/quote/")[1]

        # Remove query parameters if present
        part = part.split("?")[0]

        # Remove trailing slash
        part = part.rstrip("/")

        # Decode URL-encoded characters
        ticker = unquote(part)

        if ticker == "":
            raise ValueError("Ticker is empty")

        return ticker

    except Exception:
        raise ValueError("Could not extract ticker")

def fetch_last_month_prices(ticker):
    """
    Fetch last 30 days of closing prices using yfinance.
    """
    data = yf.Ticker(ticker).history(period="1wk")

    if data.empty:
        raise ValueError(f"No price data found for ticker {ticker}")

    return list(data["Close"])

def compute_statistics(prices):
    """
    Compute basic statistics for a list of prices.
    """
    return {
        "mean": statistics.mean(prices),
        "median": statistics.median(prices),
        "stdev": statistics.stdev(prices) if len(prices) > 1 else 0,
        "min": min(prices),
        "max": max(prices),
    }


def print_summary(ticker, stats):
    print(f"\n=== {ticker} ===")
    for key, value in stats.items():
        print(f"{key.capitalize()}: {value:.2f}")


if __name__ == "__main__":
    main()
