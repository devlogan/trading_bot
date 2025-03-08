def calculate_ema(df):
    """
    Calculate Exponential Moving Averages (EMA).
    """
    df["EMA_50"] = df["close"].ewm(span=50, adjust=False).mean()
    df["EMA_200"] = df["close"].ewm(span=200, adjust=False).mean()

    return df

