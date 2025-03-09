import pandas as pd
from binance.client import Client
from utils.constants import BINANCE_API_KEY, BINANCE_SECRET_KEY, SYMBOL, INTERVAL, LIMIT

# ✅ Initialize Binance Client
client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)


def get_historical_data(symbol=SYMBOL, interval=INTERVAL, limit=LIMIT):
    """
    Fetches historical candlestick data for a given symbol and interval.
    """
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(
        klines,
        columns=[
            "time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset",
            "trades",
            "taker_buy_base",
            "taker_buy_quote",
            "ignore",
        ],
    )

    # ✅ Only keep relevant columns
    df = df[["time", "open", "high", "low", "close"]].astype(float)
    return df


def get_current_price(symbol=SYMBOL):
    """
    Fetches the current price for a given trading pair from Binance.
    """
    try:
        price = float(client.get_symbol_ticker(symbol=symbol)["price"])
        print(f"✅ Current price for {symbol}: {price}")
        return price
    except Exception as e:
        print(f"❌ Error fetching current price: {e}")
        return None
