def calculate_rsi(df, period=14):
    """
    Calculate Relative Strength Index (RSI).
    """
    delta = df["close"].diff()
    
    # Handle NaN values properly
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Fill NaN values with reasonable defaults
    df["RSI"] = df["RSI"].fillna(method="bfill")  # Backfill NaN values

    return df
