from trading.orders import place_order
from indicators.moving_averages import calculate_ema
from indicators.atr import calculate_atr
from utils.data_fetcher import get_historical_data
from trading.orders import get_trade_quantity, generate_signals, get_futures_balance
from trading.risk_management import place_tp_sl
from utils.telegram_alerts import send_telegram_message
from utils.constants import *

# ✅ State Tracking for Last Trade
last_trade_time = None
last_trade_direction = None


def trade_trend_breakout(df=None):
    global last_trade_time, last_trade_direction

    if df is None:
        df = get_historical_data()

    # ✅ Calculate indicators
    df = calculate_ema(df)
    df = calculate_atr(df)
    df = generate_signals(df)

    # ✅ Use second-last row instead of last row
    last_row = df.iloc[-2]
    buy_signal = bool(last_row["buy_signal"])
    sell_signal = bool(last_row["sell_signal"])

    entry_time = last_row.name  # Timestamp of the signal candle

    # ✅ Ensure it's a new trade (not repeating within the same 15-min candle)
    is_new_trade = (last_trade_time is None) or (entry_time > last_trade_time)

    # ✅ Fetch current available balance from Binance Futures
    balance = get_futures_balance()

    if buy_signal and is_new_trade and last_trade_direction != "BUY":
        entry_price = float(last_row["close"])
        atr = float(last_row["ATR"])
        stop_loss = entry_price - (SL_MULTIPLIER * atr)
        take_profit = entry_price + (TP_MULTIPLIER * atr)
        quantity = get_trade_quantity(
            balance, RISK_PERCENT, entry_price, stop_loss, LEVERAGE
        )

        if not TEST_MODE:
            # ✅ Send Telegram notification in live trading only
            send_telegram_message(
                f"📈 *BUY SIGNAL DETECTED*\n"
                f"Price: `{entry_price}`\n"
                f"ATR: `{atr}`\n"
                f"Quantity: `{quantity}`"
            )
            place_order(SYMBOL, "BUY", quantity)

        print(f"📈 Buy Signal at {entry_price}, SL: {stop_loss}, TP: {take_profit}")

        place_tp_sl(SYMBOL, stop_loss, take_profit, "BUY")

        # ✅ Update last trade state
        last_trade_time = entry_time
        last_trade_direction = "BUY"

    elif sell_signal and is_new_trade and last_trade_direction != "SELL":
        entry_price = float(last_row["close"])
        atr = float(last_row["ATR"])
        stop_loss = entry_price + (SL_MULTIPLIER * atr)
        take_profit = entry_price - (TP_MULTIPLIER * atr)
        quantity = get_trade_quantity(
            balance, RISK_PERCENT, entry_price, stop_loss, LEVERAGE
        )

        if not TEST_MODE:
            send_telegram_message(
                f"📉 *SELL SIGNAL DETECTED*\n"
                f"Price: `{entry_price}`\n"
                f"ATR: `{atr}`\n"
                f"Quantity: `{quantity}`"
            )
            place_order(SYMBOL, "SELL", quantity)

        print(f"📉 Sell Signal at {entry_price}, SL: {stop_loss}, TP: {take_profit}")

        place_tp_sl(SYMBOL, stop_loss, take_profit, "SELL")

        # ✅ Update last trade state
        last_trade_time = entry_time
        last_trade_direction = "SELL"

    return df
