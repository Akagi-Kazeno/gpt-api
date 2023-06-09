import json

from entity.db_init import get_db_session, get_db_base, create_db_engine
from service import chat_service, gpt_image_service, completion_service, user_chat_completion_service, \
    user_chat_service, user_completion_service, user_gpt_image_service, web_chat_service, user_web_chat_service

# 导入sqlalchemy模块

# 创建一个数据库引擎，连接到数据库
engine = create_db_engine()
# 创建一个基类，用于定义表结构
Base = get_db_base()
# 创建一个会话类，用于操作数据库
Session = get_db_session()
session = Session()


def chat_db_commit(json_data: dict):
    """
    将处理过的对话json插入数据库
    :param json_data:
    :return:
    """
    data = chat_service.chat_json_to_db(json_data)
    commit_data(data)


def user_chat_db_commit(message: str):
    """
    将用户的对话输入插入数据库
    :param message:
    :return:
    """
    data = user_chat_service.user_chat_to_db(message)
    commit_data(data)


def user_chat_completion_to_db(message: dict):
    """
    将用户连续对话输入让插入数据库
    :param message:
    :return:
    """
    json_message = json.dumps(message)
    data = user_chat_completion_service.user_chat_completion_to_db(json_message)
    commit_data(data)


def completion_db_commit(json_data):
    """
    将处理过的对话json插入数据库
    :param json_data:
    :return:
    """
    data = completion_service.completion_json_to_db(json_data)
    commit_data(data)


def user_completion_db_commit(prompt: str):
    """
    将用户的对话输入插入数据库
    :param prompt:
    :return:
    """
    data = user_completion_service.user_completion_to_db(prompt)
    commit_data(data)


def gpt_image_db_commit(json_data):
    """
    将处理过的图片json插入数据库
    :param json_data:
    :return:
    """
    data = gpt_image_service.gpt_image_json_to_db(json_data)
    commit_data(data)


def user_gpt_image_db_commit(description: str):
    """
    将用户的图片描述插入数据库
    :param description:
    :return:
    """
    data = user_gpt_image_service.user_gpt_image_to_db(description)
    commit_data(data)


def web_chat_res_to_db(json_data: dict):
    """
    将web_chat_res插入数据库
    """
    data = web_chat_service.web_chat_res_to_db(json_data)
    commit_data(data)


def user_web_chat_to_db(message: str):
    data = user_web_chat_service.user_web_chat_to_db(message)
    commit_data(data)


def commit_data(data):
    """
    将数据提交至数据库
    :param data:
    :return:
    """
    try:
        session.add(data)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error occurred when committing data: {e}")
    finally:
        session.close()
