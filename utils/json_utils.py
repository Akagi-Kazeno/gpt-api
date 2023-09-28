import service.chat_service
import utils.session_utils

SYSTEM_ROLE: str = "system"
ASSISTANT_ROLE: str = "assistant"
USER_ROLE: str = "user"
SYSTEM_CONTENT: str = "You are a helpful assistant."
system_message_dict: dict = {"role": SYSTEM_ROLE, "content": SYSTEM_CONTENT}


def get_user_message():
    """
    获取当前session的用户输入内容
    :return:
    """
    session_value = utils.session_utils.get_session_value()
    user_message = service.chat_service.get_chat_obj_by_session(session_value)
    for index, message in enumerate(user_message):
        user_content_tuple = f"{message}"
        return user_content_tuple


def create_user_message_list() -> list:
    """
    将用户输入内容封装为列表
    :return:
    """
    user_message_list: list = []
    user_content = get_user_message()
    for user_message in user_content:
        user_message_dict: dict = {"role": USER_ROLE, "content": user_message[0]}
        user_message_list.append(user_message_dict)
    return user_message_list


def get_assistant_message():
    """
    获取当前session的gpt回复内容
    :return:
    """
    session_value = utils.session_utils.get_session_value()
    assistant_message = service.chat_service.get_chat_obj_by_session(session_value)
    for index, message in enumerate(assistant_message):
        assistant_content_tuple = f"{message}"
        return assistant_content_tuple


def create_assistant_message_list():
    """
    将gpt回复内容封装为列表
    :return:
    """
    assistant_message_list: list = []
    assistant_content = get_assistant_message()
    for assistant_message in assistant_content:
        assistant_message_dict: dict = {"role": ASSISTANT_ROLE, "content": assistant_message[0]}
        assistant_message_list.append(assistant_message_dict)
    return assistant_message_list


def get_message_list():
    """
    获取消息列表
    :return:
    """
    user_message_list: list = create_user_message_list()
    assistant_message_list: list = create_assistant_message_list()
    # 使用zip函数和列表推导式将两个列表交叉合并
    message_list: list = [x for t in zip(user_message_list, assistant_message_list) for x in t]
    # 将用户输入的最后一个元素添加到结果列表中
    message_list.append(user_message_list[-1])
    # 将系统信息添加至开头
    message_list.insert(0, system_message_dict)
    return message_list


def create_user_primer_message_list(message: str):
    """
    创建初始化对话列表
    :param message:
    :return:
    """
    primer_message_list: list = [{"role": USER_ROLE, "content": message}]
    primer_message_list.insert(0, system_message_dict)
    return primer_message_list


def create_user_chat_message_list(message: str):
    """
    创建用户对话列表
    :param message:
    :return:
    """
    user_message_list: list = create_user_message_list()
    if len(user_message_list) == 0:
        user_message_list = create_user_primer_message_list(message)
    else:
        assistant_message_list: list = create_assistant_message_list()
        # 使用zip函数和列表推导式将两个列表交叉合并
        user_chat_message_list: list = [x for t in zip(user_message_list, assistant_message_list) for x in t]
        # 将用户问题封装为字典
        user_chat_message_dict: dict = {"role": USER_ROLE, "content": message}
        # 将用户输入加入列表
        user_chat_message_list.append(user_chat_message_dict)
        # 将系统信息添加至开头
        user_chat_message_list.insert(0, system_message_dict)
    return user_message_list
