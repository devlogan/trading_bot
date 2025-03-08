from binance.client import Client
from utils.constants import BINANCE_API_KEY, BINANCE_SECRET_KEY

client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

from indicators.moving_averages import calculate_ema
from indicators.atr import calculate_atr

def generate_signals(df):
    """
    Generate buy/sell signals but prevent consecutive signals in the same direction.
    """
    df = calculate_ema(df)
    df = calculate_atr(df)

    # Generate raw signals based on EMA crossover
    df["raw_buy_signal"] = (df["EMA_50"] > df["EMA_200"]) & (df["close"] > df["high"].rolling(20).max().shift(1))
    df["raw_sell_signal"] = (df["EMA_50"] < df["EMA_200"]) & (df["close"] < df["low"].rolling(20).min().shift(1))

    # Initialize buy/sell signal columns
    df["buy_signal"] = False
    df["sell_signal"] = False

    # Track last executed trade (buy or sell)
    last_trade = None  # "BUY" or "SELL"

    for i in range(1, len(df)):
        if df["raw_buy_signal"].iloc[i] and last_trade != "BUY":
            df.at[df.index[i], "buy_signal"] = True
            last_trade = "BUY"  # Mark that a buy was executed

        elif df["raw_sell_signal"].iloc[i] and last_trade != "SELL":
            df.at[df.index[i], "sell_signal"] = True
            last_trade = "SELL"  # Mark that a sell was executed

    print(f"DEBUG: Buy Signals: {df['buy_signal'].sum()}, Sell Signals: {df['sell_signal'].sum()}")

    return df


def get_trade_quantity(balance, risk_percent, entry_price, stop_loss, leverage=10):
    """Dynamically calculate position size based on risk percentage."""
    risk_amount = balance * (risk_percent / 100)
    trade_risk = abs(entry_price - stop_loss)
    quantity = (risk_amount * leverage) / trade_risk
    return round(quantity, 3)



def place_order(symbol, side, quantity):
    """Place a Binance Futures market order"""
    quantity = float(quantity)  # Ensure quantity is a number
    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type="MARKET",
        quantity=quantity
    )
    print(f"✅ {side} Order Placed: {order}")
    return order

