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
INTERVAL = "5m"
LIMIT = 100
WAIT_TIME = 60

# ✅ Trading Settings
TRADE_AMOUNT = 50  # % of capital per trade
LEVERAGE = 10
SL_MULTIPLIER = 1.5  # Stop Loss multiplier based on ATR
TP_MULTIPLIER = 2  # Take Profit multiplier based on ATR

# ✅ EMA Configuration
EMA_SHORT_PERIOD = 20
EMA_LONG_PERIOD = 50

# ✅ Rolling window for breakout confirmation
BREAKOUT_WINDOW = 10

# ✅ Modes
TEST_MODE = False  # Set to True for backtesting/simulation

# ✅ Logging Config
LOG_LEVEL = "INFO"


