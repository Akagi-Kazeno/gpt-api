from entity.user_chat_entity import UserChat, create_session
from utils.id_utils import simple_uuid
from utils.session_utils import get_session_value, create_new_session
from utils.time_utils import timestamp_to_db


def user_chat_to_db(message: str):
    """
    将用户的聊天输入插入数据库
    :param message:
    :return:
    """
    user_chat_obj = UserChat()
    user_chat_obj.id = simple_uuid()
    if user_chat_obj.session is None or not user_chat_obj.session:
        user_chat_obj.session = create_new_session()
    else:
        user_chat_obj.session = get_session_value()
    user_chat_obj.message = message
    user_chat_obj.create_time = timestamp_to_db()
    return user_chat_obj


def get_user_chat_by_session(session_value):
    """
    获取数据库中相同session的用户对话
    :param session_value:
    :return:
    """
    session = create_session()
    user_chat_obj = session.query(UserChat.message).filter(UserChat.session == session_value).order_by(
        UserChat.create_time).all()
    return user_chat_obj


def count_user_chat_by_session(session_value):
    """
    计算数据库中相同session的用户对话数量
    :param session_value:
    :return:
    """
    user_chat_count: int = len(get_user_chat_by_session(session_value))
    return user_chat_count
