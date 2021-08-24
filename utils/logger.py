import datetime
import json
import logging
import re
import uuid

import emoji
from colorama import Fore
from pathlib import Path

with open("./config.json", "r") as config:
    config = json.load(config)

session_id = str(uuid.uuid4())


class CustomFormatter(logging.Formatter):

    format = f"%(asctime)s - %(levelname)s - [%(funcName)s]: %(emoji)s %(message)s"

    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: Fore.GREEN + format + reset,
        logging.INFO: Fore.GREEN + format + reset,
        logging.WARNING: Fore.RED + format + reset,
        logging.ERROR: Fore.RED + format + reset,
        logging.CRITICAL: Fore.RED + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("Chifuyu")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

class RemoveNoise(logging.Filter):
    def __init__(self):
        super().__init__(name='discord.state')

    def filter(self, record):
        if record.levelname == 'WARNING' and 'referencing an unknown' in record.msg:
            return False
        return True




