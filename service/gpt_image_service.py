from entity.gpt_image_entity import GptImage, create_session
from utils.id_utils import simple_uuid
from utils.session_utils import get_session_value, create_new_session
from utils.time_utils import timestamp_to_db


def gpt_image_json_to_db(json_data):
    """
    处理gpt生成图片返回的json并返回数据库
    :param json_data:
    :return:
    """
    for data in json_data['data']:
        gpt_image_obj = GptImage()
        gpt_image_obj.id = simple_uuid()
        gpt_image_obj.created = json_data['created']
        gpt_image_obj.b64_image = data['b64_json']
        if gpt_image_obj.session is None:
            gpt_image_obj.session = create_new_session()
        else:
            gpt_image_obj.session = get_session_value()
        gpt_image_obj.create_time = timestamp_to_db()
        # 将gpt_image_obj对象添加到会话中
        return gpt_image_obj


def get_gpt_image_by_session(session_value):
    """
    获取数据库中相同的session生成的image
    :param session_value:
    :return:
    """
    session = create_session()
    gpt_image_obj = session.query(GptImage.id).filter(GptImage.session == session_value).order_by(
        GptImage.create_time).all()
    return gpt_image_obj


def count_gpt_image_by_session(session_value):
    """
    计算数据库中相同session生成的image数量
    :param session_value:
    :return:
    """
    count_gpt_image: int = len(get_gpt_image_by_session(session_value))
    return count_gpt_image
