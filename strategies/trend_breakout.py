from trading.orders import place_order
from indicators.moving_averages import calculate_ema
from indicators.atr import calculate_atr
from utils.data_fetcher import get_historical_data
from trading.orders import get_trade_quantity, generate_signals
from trading.risk_management import place_tp_sl
from utils.telegram_alerts import send_telegram_message
from utils.constants import *

def trade_trend_breakout(df=None):
    if df is None:
        df = get_historical_data()

    # ✅ Calculate indicators
    df = calculate_ema(df)
    df = calculate_atr(df)
    df = generate_signals(df)

    # ✅ Use second-last row instead of last row
    last_row = df.iloc[-2]  # <-- FIXED HERE
    buy_signal = bool(last_row["buy_signal"])
    sell_signal = bool(last_row["sell_signal"])

    if buy_signal:
        entry_price = float(last_row["close"])
        atr = float(last_row["ATR"])
        quantity = get_trade_quantity(50, entry_price, 10)

        stop_loss = entry_price - (1.5 * atr)
        take_profit = entry_price + (2 * atr)

        if not TEST_MODE:
            # ✅ Send Telegram notification in live trading only
            send_telegram_message(
                f"📈 *BUY SIGNAL DETECTED*\n"
                f"Price: `{entry_price}`\n"
                f"ATR: `{atr}`\n"
                f"Quantity: `{quantity}`"
            )
            # place_order("BTCUSDT", "BUY", quantity)

        print(f"📈 Buy Signal at {entry_price}, SL: {stop_loss}, TP: {take_profit}")

        # ✅ Set SL/TP even in backtesting
        place_tp_sl("BTCUSDT", quantity, stop_loss, take_profit, "BUY")

    elif sell_signal:
        entry_price = float(last_row["close"])
        atr = float(last_row["ATR"])
        quantity = get_trade_quantity(50, entry_price, 10)

        stop_loss = entry_price + (1.5 * atr)
        take_profit = entry_price - (2 * atr)

        if not TEST_MODE:
            send_telegram_message(
                f"📉 *SELL SIGNAL DETECTED*\n"
                f"Price: `{entry_price}`\n"
                f"ATR: `{atr}`\n"
                f"Quantity: `{quantity}`"
            )
            # place_order("BTCUSDT", "SELL", quantity)

        print(f"📉 Sell Signal at {entry_price}, SL: {stop_loss}, TP: {take_profit}")

        place_tp_sl("BTCUSDT", quantity, stop_loss, take_profit, "SELL")

    return df

