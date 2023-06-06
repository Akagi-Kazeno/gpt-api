import time
from datetime import datetime

from entity.completion_entity import Completion, create_session
from utils.session_utils import get_session_value


def completion_json_to_db(json_data):
    """
    处理对话返回的json并插入数据库
    :param json_data:
    :return:
    """
    for choice in json_data['choices']:
        completion_obj = Completion()
        completion_obj.id = json_data['id']
        completion_obj.model = json_data['model']
        completion_obj.object = json_data['object']
        completion_obj.created = json_data['created']
        completion_obj.finish_reason = choice['finish_reason']
        completion_obj.index = choice['index']
        completion_obj.logprobs = choice['logprobs']
        completion_obj.text = choice['text']
        completion_obj.completion_tokens = json_data['usage']['completion_tokens']
        completion_obj.prompt_tokens = json_data['usage']['prompt_tokens']
        completion_obj.total_tokens = json_data['usage']['total_tokens']
        completion_obj.session = get_session_value()
        timestamp = datetime.fromtimestamp(time.time())
        completion_obj.create_time = timestamp
        # 将completion对象添加到会话中
        return completion_obj


def get_completion_by_session(session_value):
    """
    获取数据库中相同session的对话内容
    :param session_value:
    :return:
    """
    session = create_session()
    completion_obj = session.query(Completion.text).filter(Completion.session == session_value).order_by(
        Completion.create_time).all()
    return completion_obj


def count_completion_by_session(session_value):
    """
    计算数据库中相同session的对话数量
    :param session_value:
    :return:
    """
    completion_count: int = len(get_completion_by_session(session_value))
    return completion_count
