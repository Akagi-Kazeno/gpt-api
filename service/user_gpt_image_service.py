from entity.user_gpt_image_entity import UserGptImage, create_session
from utils.id_utils import simple_uuid
from utils.session_utils import get_session_value, create_new_session
from utils.time_utils import timestamp_to_db


def user_gpt_image_to_db(description: str):
    """
    将用户的图片描述输入插入数据库
    :param description:
    :return:
    """
    user_gpt_image_obj = UserGptImage()
    user_gpt_image_obj.id = simple_uuid()
    if user_gpt_image_obj.session is None:
        user_gpt_image_obj.session = create_new_session()
    else:
        user_gpt_image_obj.session = get_session_value()
    user_gpt_image_obj.description = description
    user_gpt_image_obj.create_time = timestamp_to_db()
    return user_gpt_image_obj


def get_user_gpt_image_by_session(session_value):
    """
    获取数据库中相同session的图片描述
    :param session_value:
    :return:
    """
    session = create_session()
    gpt_image_obj = session.query(UserGptImage.description).filter(UserGptImage.session == session_value).order_by(
        UserGptImage.create_time).all()
    return gpt_image_obj


def count_user_gpt_image_by_session(session_value):
    """
    计算数据库中相同session的图片描述
    :param session_value:
    :return:
    """
    gpt_image_count: int = len(get_user_gpt_image_by_session(session_value))
    return gpt_image_count
