from entity.user_completion_entity import UserCompletion, create_session
from utils.id_utils import simple_uuid
from utils.session_utils import get_session_value, create_session_id
from utils.time_utils import timestamp_to_db


def user_completion_to_db(prompt: str):
    """
    将用户的聊天输入插入数据库
    :param prompt:
    :return:
    """
    user_completion_obj = UserCompletion()
    user_completion_obj.id = simple_uuid()
    if user_completion_obj.session is None:
        create_session_id()
        user_completion_obj.session = get_session_value()
    else:
        user_completion_obj.session = get_session_value()
    user_completion_obj.prompt = prompt
    user_completion_obj.create_time = timestamp_to_db()
    return user_completion_obj


def get_user_completion_by_session(session_value):
    """
    获取数据库中相同session的用户对话
    :param session_value:
    :return:
    """
    session = create_session()
    user_completion_obj = session.query(UserCompletion.message).filter(
        UserCompletion.session == session_value).order_by(UserCompletion.create_time).all()
    return user_completion_obj


def count_user_completion_by_session(session_value):
    """
    计算数据库中相同session的用户对话数量
    :param session_value:
    :return:
    """
    user_completion_count: int = len(get_user_completion_by_session(session_value))
    return user_completion_count
