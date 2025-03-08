import logging

def setup_logger(name):
    logging.basicConfig(filename="logs/trading_bot.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(name)
