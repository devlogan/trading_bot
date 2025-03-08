def calculate_atr(df, period=14):
    """Calculate EMA-smoothed ATR"""
    df["high_low"] = df["high"] - df["low"]
    df["high_close"] = abs(df["high"] - df["close"].shift(1))
    df["low_close"] = abs(df["low"] - df["close"].shift(1))
    df["true_range"] = df[["high_low", "high_close", "low_close"]].max(axis=1)
    df["ATR"] = df["true_range"].ewm(span=period, adjust=False).mean()  # EMA ATR
    return df
