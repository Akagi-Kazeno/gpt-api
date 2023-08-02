import datetime

from entity.access_token_entity import AccessToken, create_session
from utils.id_utils import simple_uuid
from utils.time_utils import timestamp_to_db, access_token_expire_time


def access_token_to_db(access_token: str, wxid: str | None):
    """
    处理access_token并插入数据库
    :param access_token
    :return:
    """
    access_token_db_obj = AccessToken()
    access_token_db_obj.id = simple_uuid()
    access_token_db_obj.access_token = access_token
    access_token_db_obj.create_time = timestamp_to_db()
    access_token_db_obj.expire_time = access_token_expire_time()
    access_token_db_obj.wxid = wxid
    return access_token_db_obj


def get_access_token_by_wxid(wxid: str):
    """
    获取数据库中相同wxid的access_token
    :param wxid:
    :return:
    """
    session = create_session()
    current_time = datetime.datetime.now()
    try:
        access_token = (session.query(AccessToken.access_token)
                        .filter(AccessToken.wxid == wxid, AccessToken.expire_time > current_time)
                        .order_by(AccessToken.create_time.desc()).first())
        return access_token
    except Exception as e:
        raise e
