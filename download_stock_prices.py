#!/usr/bin/env python3
"""Download stock prices and save them as NumPy arrays."""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.error import URLError

import numpy as np
import pandas as pd
from scipy import stats


def download_stooq_prices(ticker: str, start: str | None, end: str | None) -> pd.DataFrame:
    """Download daily OHLCV data for a ticker from Stooq."""
    symbol = f"{ticker.lower()}.us"
    url = f"https://stooq.com/q/d/l/?s={symbol}&i=d"

    try:
        frame = pd.read_csv(url, parse_dates=["Date"])
    except URLError as exc:
        raise RuntimeError(
            f"Unable to download data for '{ticker}'. Check your network connection and try again."
        ) from exc

    frame = frame.sort_values("Date").reset_index(drop=True)

    if start:
        frame = frame[frame["Date"] >= pd.Timestamp(start)]
    if end:
        frame = frame[frame["Date"] <= pd.Timestamp(end)]

    if frame.empty:
        raise ValueError(f"No data returned for ticker '{ticker}' in the selected range.")

    return frame


def save_arrays(prices: dict[str, np.ndarray], output_dir: Path) -> None:
    """Save per-ticker arrays and a combined matrix."""
    output_dir.mkdir(parents=True, exist_ok=True)

    ordered_tickers = list(prices)
    max_length = max(len(values) for values in prices.values())
    matrix = np.full((max_length, len(ordered_tickers)), np.nan)

    for index, ticker in enumerate(ordered_tickers):
        values = prices[ticker]
        matrix[: len(values), index] = values
        np.save(output_dir / f"{ticker.lower()}_close.npy", values)

    np.save(output_dir / "close_prices_matrix.npy", matrix)
    np.save(output_dir / "tickers.npy", np.array(ordered_tickers, dtype=object))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tickers",
        nargs="+",
        default=["AAPL", "MSFT", "GOOGL"],
        help="Ticker symbols to download (default: AAPL MSFT GOOGL)",
    )
    parser.add_argument("--start", default=None, help="Optional start date (YYYY-MM-DD)")
    parser.add_argument("--end", default=None, help="Optional end date (YYYY-MM-DD)")
    parser.add_argument(
        "--output-dir",
        default="stock_arrays",
        help="Directory where NumPy arrays are stored (default: stock_arrays)",
    )
    args = parser.parse_args()

    close_prices: dict[str, np.ndarray] = {}

    try:
        for ticker in args.tickers:
            frame = download_stooq_prices(ticker, args.start, args.end)
            close = frame["Close"].to_numpy(dtype=float)

            # Basic SciPy usage: standardized prices array.
            _ = stats.zscore(close)

            close_prices[ticker.upper()] = close
            print(f"Downloaded {ticker.upper()}: {len(close)} rows")
    except (RuntimeError, ValueError) as exc:
        raise SystemExit(str(exc))

    save_arrays(close_prices, Path(args.output_dir))
    print(f"Saved arrays to: {Path(args.output_dir).resolve()}")


if __name__ == "__main__":
    main()
