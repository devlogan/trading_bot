from binance.client import Client
from utils.constants import BINANCE_API_KEY, BINANCE_SECRET_KEY
from indicators.moving_averages import calculate_ema
from indicators.atr import calculate_atr
from utils.constants import EMA_SHORT_PERIOD, EMA_LONG_PERIOD, BREAKOUT_WINDOW

client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

def generate_signals(df):
    """
    Generate buy/sell signals but prevent consecutive signals in the same direction.
    """
    df = calculate_ema(df)
    df = calculate_atr(df)

    # ✅ Dynamic EMA names based on constants
    ema_short = f"EMA_{EMA_SHORT_PERIOD}"
    ema_long = f"EMA_{EMA_LONG_PERIOD}"

    # ✅ Generate raw signals based on EMA crossover and breakout
    df["raw_buy_signal"] = (
        (df[ema_short] > df[ema_long]) &
        (df["close"] > df["high"].rolling(BREAKOUT_WINDOW).max().shift(1))
    )
    
    df["raw_sell_signal"] = (
        (df[ema_short] < df[ema_long]) &
        (df["close"] < df["low"].rolling(BREAKOUT_WINDOW).min().shift(1))
    )

    # ✅ Initialize buy/sell signal columns
    df["buy_signal"] = False
    df["sell_signal"] = False

    # ✅ Track last executed trade to prevent consecutive same-side signals
    last_trade = None
    
    if df["raw_buy_signal"].iloc[-2]:
        last_trade = "BUY"
    elif df["raw_sell_signal"].iloc[-2]:
        last_trade = "SELL"

    for i in range(1, len(df)):
        # ✅ Buy signal only if last trade was NOT a BUY
        if df["raw_buy_signal"].iloc[i] and last_trade != "BUY":
            df.loc[df.index[i], "buy_signal"] = True
            last_trade = "BUY"

        # ✅ Sell signal only if last trade was NOT a SELL
        elif df["raw_sell_signal"].iloc[i] and last_trade != "SELL":
            df.loc[df.index[i], "sell_signal"] = True
            last_trade = "SELL"

    # ✅ Debug output to verify signal generation
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

