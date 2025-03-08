import pandas as pd
from binance.client import Client
import time

# Binance API keys (for public data access, you don't need API keys)
api_key = "YOUR_BINANCE_API_KEY"  # Optional
api_secret = "YOUR_BINANCE_SECRET_KEY"  # Optional
client = Client(api_key, api_secret)

def fetch_binance_data(symbol="BTCUSDT", interval="1h", start_str="1 Jan, 2023", end_str="1 Mar, 2025", save_csv=True):
    """
    Fetches historical Binance OHLCV data and saves as CSV.
    :param symbol: Trading pair (e.g., "BTCUSDT")
    :param interval: Timeframe (e.g., "1h", "15m", "4h")
    :param start_str: Start date in Binance format (e.g., "1 Jan, 2023")
    :param end_str: End date in Binance format (e.g., "1 Mar, 2025")
    :param save_csv: Save as CSV file
    """
    print(f"Fetching {symbol} {interval} data from {start_str} to {end_str}...")

    # Fetch data
    klines = client.get_historical_klines(symbol, interval, start_str, end_str)

    # Convert to DataFrame
    df = pd.DataFrame(klines, columns=["time", "open", "high", "low", "close", "volume", "close_time", "quote_asset", "trades", "taker_buy_base", "taker_buy_quote", "ignore"])
    
    # Keep only necessary columns
    df = df[["time", "open", "high", "low", "close"]]
    
    # Convert timestamps
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    
    # Save CSV
    if save_csv:
        file_path = f"data/{symbol}_{interval}.csv"
        df.to_csv(file_path, index=False)
        print(f"✅ Data saved to {file_path}")

    return df

# Run the function to download data
fetch_binance_data()
