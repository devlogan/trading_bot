from utils.telegram_alerts import send_telegram_message
from utils.data_fetcher import get_current_price
from utils.constants import TEST_MODE
from binance.client import Client
from utils.constants import BINANCE_API_KEY, BINANCE_SECRET_KEY
from trading.orders import round_value

client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

def place_tp_sl(symbol, stop_loss, take_profit, side):
    print(f"Placing TP/SL for {symbol}, Side: {side}")

    # ✅ Round stop_loss and take_profit based on precision
    stop_loss = round_value(symbol, stop_loss, value_type="price")
    take_profit = round_value(symbol, take_profit, value_type="price")

    if TEST_MODE:
        current_price = get_current_price(symbol)
        stop_loss_hit = (current_price <= stop_loss) if side == "BUY" else (current_price >= stop_loss)
        take_profit_hit = (current_price >= take_profit) if side == "BUY" else (current_price <= take_profit)

        if stop_loss_hit:
            print(f"❌ Stop Loss Hit at {stop_loss}")
            send_telegram_message(f"❌ *STOP LOSS HIT*\nPrice: `{stop_loss}`")

        if take_profit_hit:
            print(f"✅ Take Profit Hit at {take_profit}")
            send_telegram_message(f"✅ *TAKE PROFIT HIT*\nPrice: `{take_profit}`")

    else:
        try:
            # ✅ Determine opposite side for closing
            close_side = Client.SIDE_SELL if side == "BUY" else Client.SIDE_BUY

            # ✅ Create stop-loss order
            stop_order = client.futures_create_order(
                symbol=symbol,
                side=close_side,
                type=Client.FUTURE_ORDER_TYPE_STOP_MARKET,
                closePosition=True,
                stopPrice=stop_loss,
                timeInForce="GTC",
            )

            # ✅ Create take-profit order
            tp_order = client.futures_create_order(
                symbol=symbol,
                side=close_side,
                type=Client.FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET,
                stopPrice=take_profit,
                closePosition=True,
                timeInForce="GTC",
            )

            print(f"✅ TP/SL order placed: TP={take_profit}, SL={stop_loss}")
            send_telegram_message(
                f"✅ *TP/SL ORDER PLACED*\n"
                f"TP: `{take_profit}`\n"
                f"SL: `{stop_loss}`"
            )

        except Exception as e:
            print(f"❌ Error placing TP/SL order: {e}")
            send_telegram_message(f"❌ *Failed to place TP/SL order*: `{e}`")