import logging
from datetime import datetime
import sys

class LocalTimeFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt, style="%")

    def formatTime(self, record, datefmt=None):
        # ✅ Convert to human-readable local time format (e.g., "Mar 08, 2025 11:06:47 PM")
        ct = datetime.fromtimestamp(record.created)
        if datefmt:
            return ct.strftime(datefmt)
        else:
            return ct.strftime("%b %d, %Y %I:%M:%S %p")  # ✅ Human-readable format

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # ✅ File handler with UTF-8 encoding
    file_handler = logging.FileHandler("logs/trading_bot.log", encoding="utf-8")
    formatter = LocalTimeFormatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # ✅ Stream handler with UTF-8 encoding
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.stream = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

    # ✅ Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
