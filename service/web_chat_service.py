from entity.web_chat_response_entity import WebChatResponseEntity
from utils.id_utils import simple_uuid
from utils.session_utils import get_session_value
from utils.time_utils import timestamp_to_db


def web_chat_res_to_db(json_data: dict):
    """
       处理对话返回的json并插入数据库
       :param json_data
       :return:
       """
    web_chat_res = WebChatResponseEntity()
    web_chat_res.web_chat_id = simple_uuid()
    web_chat_res.conversation_id = json_data['conversation_id']
    web_chat_res.end_turn = json_data['end_turn']
    web_chat_res.finish_details = json_data['finish_details']
    web_chat_res.message = json_data['message']
    web_chat_res.model = json_data['model']
    web_chat_res.parent_id = json_data['parent_id']
    web_chat_res.recipient = json_data['recipient']
    web_chat_res.session = get_session_value()
    web_chat_res.create_time = timestamp_to_db()
    # 将web_chat_res添加到会话中
    return web_chat_res
