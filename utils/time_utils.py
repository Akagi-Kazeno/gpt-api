import time
from datetime import datetime


def timestamp_to_db():
    """
    插入数据库的时间戳
    """
    timestamp = datetime.fromtimestamp(time.time())
    return timestamp


def access_token_expire_time():
    """
    access_token过期时间
    """
    expire_time = datetime.fromtimestamp(time.time() + 3600 * 24 * 30)
    return expire_time
