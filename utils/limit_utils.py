import os

from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry

load_dotenv()


@sleep_and_retry
@limits(calls=int(os.getenv("CHAT_CALLS")), period=int(os.getenv("RATE_LIMIT")))
def check_limit():
    """Empty function just to check for calls to API"""
    return
