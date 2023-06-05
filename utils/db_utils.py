import json
import os

from dotenv import load_dotenv
# 导入sqlalchemy模块
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from entity import chat_entity, completion_entity, gpt_image_entity, user_chat_entity, user_completion_entity, \
    user_gpt_image_entity, user_chat_completion_entity

load_dotenv()

# 创建一个数据库引擎，连接到gpt数据库
engine = create_engine(os.getenv("DATABASE_URL"))
# 创建一个基类，用于定义表结构
Base = declarative_base()
# 创建一个会话类，用于操作数据库
Session = sessionmaker(bind=engine)
session = Session()


def chat_db_commit(json_data: dict):
    """
    将处理过的对话json插入数据库
    :param json_data:
    :return:
    """
    data = chat_entity.chat_json_to_db(json_data)
    commit_data(data)


def user_chat_db_commit(message: str):
    """
    将用户的对话输入插入数据库
    :param message:
    :return:
    """
    data = user_chat_entity.user_chat_to_db(message)
    commit_data(data)


def user_chat_completion_to_db(message: dict):
    """
    将用户连续对话输入让插入数据库
    :param message:
    :return:
    """
    json_message = json.dumps(message)
    data = user_chat_completion_entity.user_chat_completion_to_db(json_message)
    commit_data(data)


def completion_db_commit(json_data):
    """
    将处理过的对话json插入数据库
    :param json_data:
    :return:
    """
    data = completion_entity.completion_json_to_db(json_data)
    commit_data(data)


def user_completion_db_commit(prompt: str):
    """
    将用户的对话输入插入数据库
    :param prompt:
    :return:
    """
    data = user_completion_entity.user_completion_to_db(prompt)
    commit_data(data)


def gpt_image_db_commit(json_data):
    """
    将处理过的图片json插入数据库
    :param json_data:
    :return:
    """
    data = gpt_image_entity.gpt_image_json_to_db(json_data)
    commit_data(data)


def user_gpt_image_db_commit(description: str):
    """
    将用户的图片描述插入数据库
    :param description:
    :return:
    """
    data = user_gpt_image_entity.user_gpt_image_to_db(description)
    commit_data(data)


def commit_data(data):
    """
    将数据提交至数据库
    :param data:
    :return:
    """
    session.add(data)
    session.commit()
    session.close()
