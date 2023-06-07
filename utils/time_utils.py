import time
from datetime import datetime


def timestamp_to_db():
    """
    插入数据库的时间戳
    """
    timestamp = datetime.fromtimestamp(time.time())
    return timestamp
