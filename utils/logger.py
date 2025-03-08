import logging
from datetime import datetime

class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created)  # <-- Local Time
        if datefmt:
            return ct.strftime(datefmt)
        else:
            return ct.isoformat()

# Example:
formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s')
