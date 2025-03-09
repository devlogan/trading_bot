from binance.client import Client
from binance.exceptions import BinanceAPIException
from utils.constants import BINANCE_API_KEY, BINANCE_SECRET_KEY
from indicators.moving_averages import calculate_ema
from indicators.atr import calculate_atr
from utils.constants import EMA_SHORT_PERIOD, EMA_LONG_PERIOD, BREAKOUT_WINDOW, SYMBOL
from decimal import Decimal, ROUND_DOWN
from utils.telegram_alerts import send_telegram_message
from utils.data_fetcher import get_current_price


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
    df["raw_buy_signal"] = (df[ema_short] > df[ema_long]) & (
        df["close"] > df["high"].rolling(BREAKOUT_WINDOW).max().shift(1)
    )

    df["raw_sell_signal"] = (df[ema_short] < df[ema_long]) & (
        df["close"] < df["low"].rolling(BREAKOUT_WINDOW).min().shift(1)
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
    print(
        f"DEBUG: Buy Signals: {df['buy_signal'].sum()}, Sell Signals: {df['sell_signal'].sum()}"
    )

    return df


def get_trade_quantity(balance, risk_percent, entry_price, stop_loss, leverage=10):
    """Dynamically calculate position size based on risk percentage."""
    risk_amount = balance * (risk_percent / 100)  # Risk amount in USDT
    symbol_current_price = get_current_price(SYMBOL)

    if symbol_current_price <= 0:
        return 0  # Prevent invalid quantity calculation

    quantity = (risk_amount * leverage) / symbol_current_price  # Correct formula

    # ✅ Debugging
    print(
        f"DEBUG: Risk Amount: {risk_amount}, Leverage: {leverage}, Symbol Price: {symbol_current_price}, Quantity: {quantity}"
    )

    return round(quantity, 3)


def place_order(symbol, side, quantity):
    """Place a Binance Futures market order"""
    try:
        quantity = round_quantity(symbol, quantity)

        if quantity <= 0:
            print(f"⚠️ Invalid order quantity: {quantity}")
            return

        # ✅ Actual Order Execution
        order = client.futures_create_order(
            symbol=symbol, side=side, type="MARKET", quantity=quantity
        )
        print(f"✅ {side} Order Placed: {order}")

        return order

    except BinanceAPIException as e:
        print(f"❌ BinanceAPIException: Code: {e.code}, Message: {e.message}")
        if e.code == -2019:
            print(f"⚠️ Insufficient margin for order: {quantity}")
            send_telegram_message(f"⚠️ *Insufficient Margin*\n{e.message}")
        elif e.code == -4003:
            print(f"⚠️ Invalid order quantity: {quantity}")
            send_telegram_message(
                f"⚠️ *Invalid Quantity*\nQuantity: `{quantity}`\nError: `{e.message}`"
            )
        else:
            print(f"❌ Error placing order: {e.message}")
            send_telegram_message(f"❌ *Failed to place order*: `{e.message}`")

    except Exception as e:
        print(f"❌ General Error: {e}")
        send_telegram_message(f"❌ *General Error*: `{e}`")


def get_futures_balance():
    """Fetch available balance from Binance Futures"""
    try:
        balance_info = client.futures_account_balance()
        for asset in balance_info:
            if asset["asset"] == "USDT":
                available_balance = float(asset["availableBalance"])
                return available_balance
        return 0
    except Exception as e:
        print(f"❌ Error fetching futures balance: {e}")
        return 0


def round_quantity(symbol, quantity):
    info = client.futures_exchange_info()
    for symbol_info in info["symbols"]:
        if symbol_info["symbol"] == symbol:
            step_size = Decimal(
                symbol_info["filters"][2]["stepSize"]
            )  # Use Decimal for accuracy
            rounded_quantity = Decimal(quantity).quantize(
                step_size, rounding=ROUND_DOWN
            )
            return float(rounded_quantity)
    return quantity


def round_value(symbol, value, value_type="quantity"):
    """
    Round value based on Binance Futures precision:
    - value_type="quantity" → for position size
    - value_type="price" → for price precision
    """
    info = client.futures_exchange_info()

    for symbol_info in info["symbols"]:
        if symbol_info["symbol"] == symbol:
            if value_type == "quantity":
                step_size = symbol_info["filters"][2]["stepSize"]
                precision = Decimal(str(step_size)).normalize().as_tuple().exponent * -1
            elif value_type == "price":
                tick_size = symbol_info["filters"][0]["tickSize"]
                precision = Decimal(str(tick_size)).normalize().as_tuple().exponent * -1
            else:
                raise ValueError("Invalid value_type. Use 'quantity' or 'price'.")

            # ✅ Use Python's round with calculated precision
            return round(value, precision)

    raise Exception(f"Failed to fetch symbol info for {symbol}")
