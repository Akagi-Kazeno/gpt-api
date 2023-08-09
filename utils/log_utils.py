import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

load_dotenv()


def create_log(filename: str):
    """
    创建log
    :param filename:
    :return:
    """
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s')
    log_path = os.getenv("LOG_PATH")
    max_log_size = 10 * 1024 * 1024
    log_file = RotatingFileHandler(log_path + filename, maxBytes=max_log_size, backupCount=10, encoding="utf-8")
    log_file.setFormatter(formatter)
    logger.addHandler(log_file)
    return logger
