# Econometrics_Portfolio
Projects on Econometrics and related quantitative Research stuff.

## Download stock prices to arrays

Use `download_stock_prices.py` to download stock price data with pandas and save arrays with NumPy.
The script also uses SciPy for basic processing.

```bash
python download_stock_prices.py --tickers AAPL MSFT GOOGL --start 2023-01-01 --end 2024-12-31
```

This creates a `stock_arrays/` directory with one `.npy` array per ticker plus a combined matrix.
