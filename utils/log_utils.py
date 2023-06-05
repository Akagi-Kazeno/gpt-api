import logging
import os

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
    log_file = logging.FileHandler(os.getenv("LOG_PATH") + filename, encoding="utf-8")
    log_file.setFormatter(formatter)
    logger.addHandler(log_file)
    return logger
