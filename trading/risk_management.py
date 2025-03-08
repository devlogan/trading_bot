from utils.telegram_alerts import send_telegram_message
from utils.data_fetcher import get_current_price

TEST_MODE = False

def place_tp_sl(symbol, quantity, stop_loss, take_profit, side):
    print(f"Placing TP/SL for {symbol}, Side: {side}")

    # Simulate SL/TP hits for backtesting
    stop_loss_hit = False
    take_profit_hit = False

    current_price = get_current_price(symbol) if not TEST_MODE else None
    
    if side == "BUY":
        if TEST_MODE:  # Simulate for backtest using historical data
            stop_loss_hit = current_price <= stop_loss if current_price else False
            take_profit_hit = current_price >= take_profit if current_price else False
        else:
            stop_loss_hit = current_price <= stop_loss
            take_profit_hit = current_price >= take_profit

        if stop_loss_hit:
            print(f"❌ Stop Loss Hit at {stop_loss}")
            if not TEST_MODE:
                send_telegram_message(f"❌ *STOP LOSS HIT*\nPrice: `{stop_loss}`")
        
        if take_profit_hit:
            print(f"✅ Take Profit Hit at {take_profit}")
            if not TEST_MODE:
                send_telegram_message(f"✅ *TAKE PROFIT HIT*\nPrice: `{take_profit}`")

    elif side == "SELL":
        if TEST_MODE:
            stop_loss_hit = current_price >= stop_loss if current_price else False
            take_profit_hit = current_price <= take_profit if current_price else False
        else:
            stop_loss_hit = current_price >= stop_loss
            take_profit_hit = current_price <= take_profit

        if stop_loss_hit:
            print(f"❌ Stop Loss Hit at {stop_loss}")
            if not TEST_MODE:
                send_telegram_message(f"❌ *STOP LOSS HIT*\nPrice: `{stop_loss}`")
        
        if take_profit_hit:
            print(f"✅ Take Profit Hit at {take_profit}")
            if not TEST_MODE:
                send_telegram_message(f"✅ *TAKE PROFIT HIT*\nPrice: `{take_profit}`")

