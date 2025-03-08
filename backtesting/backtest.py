import sys
import os

# Add project root directory to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from strategies.trend_breakout import generate_signals
from indicators.moving_averages import calculate_ema
from indicators.atr import calculate_atr

def load_historical_data(filepath="data/BTCUSDT_1h.csv"):
    """
    Loads historical data from CSV and converts the time column to datetime format.
    """
    df = pd.read_csv(filepath)

    # Convert time column to datetime
    df["time"] = pd.to_datetime(df["time"])  # Removed unit="ms"

    # Set the time column as the index for easier analysis
    df.set_index("time", inplace=True)

    return df

def backtest_strategy(df, initial_balance=1000, leverage=10):
    balance = initial_balance
    position = 0
    trade_log = []
    balance_over_time = []  # Track balance at each trade

    stop_loss = None
    take_profit = None

    for i in range(len(df)):
        row = df.iloc[i]
        entry_price = row["close"]
        trade_amount = balance * 0.10
        quantity = (trade_amount * leverage) / entry_price

        # Simulate SL/TP for backtest
        stop_loss_hit = False
        take_profit_hit = False

        if position > 0:  # Long position
            stop_loss_hit = row["low"] <= stop_loss if stop_loss else False
            take_profit_hit = row["high"] >= take_profit if take_profit else False

            if stop_loss_hit:
                balance -= trade_amount
                position = 0
                trade_log.append(("STOP LOSS HIT", stop_loss, row.name, balance))
                print(f"❌ Stop Loss Hit at {stop_loss}, Balance: ${balance:.2f}")

            if take_profit_hit:
                balance += trade_amount * 2
                position = 0
                trade_log.append(("TAKE PROFIT HIT", take_profit, row.name, balance))
                print(f"✅ Take Profit Hit at {take_profit}, Balance: ${balance:.2f}")

        elif position < 0:  # Short position
            stop_loss_hit = row["high"] >= stop_loss if stop_loss else False
            take_profit_hit = row["low"] <= take_profit if take_profit else False

            if stop_loss_hit:
                balance -= trade_amount
                position = 0
                trade_log.append(("STOP LOSS HIT", stop_loss, row.name, balance))
                print(f"❌ Stop Loss Hit at {stop_loss}, Balance: ${balance:.2f}")

            if take_profit_hit:
                balance += trade_amount * 2
                position = 0
                trade_log.append(("TAKE PROFIT HIT", take_profit, row.name, balance))
                print(f"✅ Take Profit Hit at {take_profit}, Balance: ${balance:.2f}")

        # Open new trade if conditions match
        if row["buy_signal"] and position == 0:
            position = quantity
            stop_loss = entry_price - (1.5 * row["ATR"])
            take_profit = entry_price + (2 * row["ATR"])
            trade_log.append(("BUY", entry_price, stop_loss, take_profit, row.name, balance))
            print(f"📈 BUY at {entry_price}, SL: {stop_loss}, TP: {take_profit}, Balance: ${balance:.2f}")

        elif row["sell_signal"] and position == 0:
            position = -quantity
            stop_loss = entry_price + (1.5 * row["ATR"])
            take_profit = entry_price - (2 * row["ATR"])
            trade_log.append(("SELL", entry_price, stop_loss, take_profit, row.name, balance))
            print(f"📉 SELL at {entry_price}, SL: {stop_loss}, TP: {take_profit}, Balance: ${balance:.2f}")

        # Log balance over time
        balance_over_time.append((row.name, balance))

    # Convert to DataFrame for better visualization
    balance_df = pd.DataFrame(balance_over_time, columns=["Time", "Balance"])

    return balance, trade_log, balance_df


if __name__ == "__main__":
    df = load_historical_data()

    # ✅ Use the same signal generation logic from trend_breakout.py
    df = calculate_ema(df)
    df = calculate_atr(df)
    df = generate_signals(df)

    print("DEBUG: First 5 Rows After Signal Generation:\n", df.head())

    final_balance, trade_log, balance_df = backtest_strategy(df)

    print(f"📈 Final Balance: ${final_balance:.2f}")
    print("Trade Log (First 10 Trades):")
    for trade in trade_log[:10]:  # Print only first 10 trades for debugging
        print(trade)

    # Save balance over time
    balance_df.to_csv("balance_over_time.csv", index=False)
    print("✅ Balance data saved to balance_over_time.csv")

    # Plot Balance Over Time
    plt.figure(figsize=(10, 5))
    plt.plot(balance_df["Time"], balance_df["Balance"], label="Balance", color="blue")
    plt.xlabel("Time")
    plt.ylabel("Balance ($)")
    plt.title("Trading Strategy Performance Over Time")
    plt.legend()
    plt.grid()
    plt.show()


def plot_trades(df, trade_log):
    plt.figure(figsize=(12,6))
    plt.plot(df.index, df["close"], label="Price", color="black")

    # Plot Buy Trades
    for trade in trade_log:
        if trade[0] == "BUY":
            plt.scatter(trade[4], trade[1], marker="^", color="green", label="Buy Signal", s=100)
        elif trade[0] == "SELL":
            plt.scatter(trade[4], trade[1], marker="v", color="red", label="Sell Signal", s=100)

    plt.legend()
    plt.title("Trading Strategy Performance")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.show()

# ✅ Run plotting
plot_trades(df, trade_log)
