import pandas as pd

def calculate_rsi(df, period=14):
    """Calculate RSI (Relative Strength Index)"""
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    return df

df = calculate_rsi(df)

# Buy only when RSI is below 30 (oversold) and EMA crossover is bullish
df["buy_signal"] = (df["EMA_50"] > df["EMA_200"]) & (df["close"] > df["high"].rolling(20).max().shift(1)) & (df["RSI"] < 30)

# Sell only when RSI is above 70 (overbought) and EMA crossover is bearish
df["sell_signal"] = (df["EMA_50"] < df["EMA_200"]) & (df["close"] < df["low"].rolling(20).min().shift(1)) & (df["RSI"] > 70)
