from utils.constants import EMA_SHORT_PERIOD, EMA_LONG_PERIOD

def calculate_ema(df):
    """
    Calculate Exponential Moving Averages (EMA) using configurable periods.
    """
    df[f"EMA_{EMA_SHORT_PERIOD}"] = df["close"].ewm(span=EMA_SHORT_PERIOD, adjust=False).mean()
    df[f"EMA_{EMA_LONG_PERIOD}"] = df["close"].ewm(span=EMA_LONG_PERIOD, adjust=False).mean()

    return df


