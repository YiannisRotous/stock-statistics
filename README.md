# stock-statistics
Stock Statistics is a Python application that allows users to input multiple Yahoo Finance stock URLs, validates each URL, extracts the corresponding ticker symbol, downloads recent price data using the yfinance library, and computes basic descriptive statistics for each asset.
The project dedicated as a final submission for CS50’s Introduction to Computer Science, following all structural and testing requirements, displayed there.

# features

- Accepts multiple Yahoo Finance URLs until the user types done
- Validates each URL using an HTTP request with a browser-like User-Agent
- Extracts tickers from all Yahoo Finance formats, including encoded tickers
- Fetches weekly closing prices using yfinance
- Computes: Mean price, Median price, Standard deviation, Minimum price, Maximum price
- Prints a clean summary for each ticker
- Includes ```pytest``` unit tests for core functions: ```extract_ticker```, ```is_valid_url```, ```compute_statistics```

# usage

Run the program:

```python project.py```

You will be prompted to enter stock URLs:

```
Enter stock URLs (type 'done' to finish):
URL: https://finance.yahoo.com/quote/AAPL/
URL accepted.
URL: https://finance.yahoo.com/quote/%5EVIX/
URL accepted.
URL: done
```

The program will then fetch weekly closing prices and compute statistics:

```
=== AAPL ===
Mean: 175.12
Median: 175.30
Stdev: 1.45
Min: 172.88
Max: 177.90

=== ^VIX ===
Mean: 14.22
Median: 14.10
Stdev: 0.85
Min: 13.20
Max: 15.40
```

# last remarks

By no means this algorithm should be used as an inference, tool it was mainly created for fun and to fresh up my skills!
