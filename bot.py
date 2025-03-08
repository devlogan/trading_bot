from strategies.trend_breakout import trade_trend_breakout
from utils.logger import setup_logger
import time
from utils.constants import WAIT_TIME

logger = setup_logger("trading_bot")


while True:
    try:
        logger.info("🔍 Checking for trade opportunities...")
        trade_trend_breakout()
        logger.info(f"⏳ Waiting for {WAIT_TIME} seconds before the next check...")
        time.sleep(WAIT_TIME)  # Check every 5 minutes
    except Exception as e:
        logger.error(f"⚠️ Error: {e}")
        time.sleep(10)  # Wait 10 sec before retrying after an error
