from entity.user_chat_completion_entity import UserChatCompletion, create_session
from utils.id_utils import simple_uuid
from utils.session_utils import get_session_value, create_session_id
from utils.time_utils import timestamp_to_db


def user_chat_completion_to_db(message):
    """
    将用户的聊天输入插入数据库
    :param message:
    :return:
    """
    user_chat_obj = UserChatCompletion()
    user_chat_obj.id = simple_uuid()
    if user_chat_obj.session is None:
        create_session_id()
        user_chat_obj.session = get_session_value()
    else:
        user_chat_obj.session = get_session_value()
    user_chat_obj.message = message
    user_chat_obj.create_time = timestamp_to_db()
    return user_chat_obj


def get_user_chat_completion_by_session(session_value):
    """
    获取数据库中相同session的用户对话
    :param session_value:
    :return:
    """
    session = create_session()
    user_chat_obj = session.query(UserChatCompletion.message).filter(
        UserChatCompletion.session == session_value).order_by(UserChatCompletion.create_time).all()
    return user_chat_obj


def count_user_chat_completion_by_session(session_value):
    """
    计算数据库中相同session的用户对话数量
    :param session_value:
    :return:
    """
    user_chat_count: int = len(get_user_chat_completion_by_session(session_value))
    return user_chat_count
