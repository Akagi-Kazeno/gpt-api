from entity.chat_entity import create_session, Chat
from utils.session_utils import create_new_session, get_session_value
from utils.time_utils import timestamp_to_db


def chat_json_to_db(json_data: dict):
    """
    处理对话返回的json并插入数据库
    :param json_data:
    :return:
    """
    for choice in json_data['choices']:
        chat_obj = Chat()
        chat_obj.id = json_data['id']
        chat_obj.model = json_data['model']
        chat_obj.object = json_data['object']
        chat_obj.created = json_data['created']
        chat_obj.finish_reason = choice['finish_reason']
        chat_obj.index = choice['index']
        chat_obj.content = choice['message']['content']
        chat_obj.role = choice['message']['role']
        chat_obj.completion_tokens = json_data['usage']['completion_tokens']
        chat_obj.prompt_tokens = json_data['usage']['prompt_tokens']
        chat_obj.total_tokens = json_data['usage']['total_tokens']
        if chat_obj.session is None:
            chat_obj.session = create_new_session()
        else:
            chat_obj.session = get_session_value()
        chat_obj.create_time = timestamp_to_db()
        # 将chat对象添加到会话中
        return chat_obj


def get_chat_obj_by_session(session_value):
    """
    获取数据库中相同session的对话内容
    :param session_value:
    :return:
    """
    session = create_session()
    chat_obj = session.query(Chat.content).filter(Chat.session == session_value).order_by(
        Chat.create_time).all()
    return chat_obj


def count_chat_by_session(session_value):
    """
    计算数据库中相同session的对话
    :param session_value:
    :return:
    """
    chat_count: int = len(get_chat_obj_by_session(session_value))
    return chat_count
