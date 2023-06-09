from entity.user_web_chat_entiy import UserWebChat
from utils.id_utils import simple_uuid
from utils.session_utils import get_session_value
from utils.time_utils import timestamp_to_db


def user_web_chat_to_db(message: str):
    user_web_chat_obj = UserWebChat()
    user_web_chat_obj.id = simple_uuid()
    user_web_chat_obj.message = message
    user_web_chat_obj.session = get_session_value()
    user_web_chat_obj.create_time = timestamp_to_db()
    return user_web_chat_obj
