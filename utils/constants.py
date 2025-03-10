from dotenv import load_dotenv
import os

# ✅ Load .env file
load_dotenv()

# ✅ Binance API Keys
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# ✅ Telegram Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ✅ General Config
SYMBOL = "BTCUSDT"
INTERVAL = "15m"  # 15-minute candles = Best for EMA + ATR combo
LIMIT = 100
WAIT_TIME = 300  # Check every 300 seconds, 5 minutes

# ✅ Trading Settings
RISK_PERCENT = 60  # % of capital per trade
LEVERAGE = 10  # Controlled leverage for lower risk
SL_MULTIPLIER = 2  # Slightly loose SL for trend-following
TP_MULTIPLIER = 3  # Take profit at 3x ATR-based volatility

# ✅ EMA Configuration
EMA_SHORT_PERIOD = 20  # Faster EMA for crossover
EMA_LONG_PERIOD = 50  # Slower EMA for trend detection

# ✅ Breakout Configuration
BREAKOUT_WINDOW = 20  # Look at last 20 candles for breakout confirmation

# ✅ Modes
TEST_MODE = False

# ✅ Logging Config
LOG_LEVEL = "INFO"



