import os
import time
from datetime import datetime

from dotenv import load_dotenv
# 导入sqlalchemy模块
from sqlalchemy import create_engine, Column, String, Text, DATETIME
from sqlalchemy.orm import sessionmaker, declarative_base

import utils.session_utils

load_dotenv()

# 创建一个数据库引擎，连接到gpt数据库
engine = create_engine(os.getenv("DATABASE_URL"))
# 创建一个基类，用于定义表结构
Base = declarative_base()
# 创建一个会话类，用于操作数据库
Session = sessionmaker(bind=engine)


# 定义一个chat类，对应于chat表
class Chat(Base):
    __tablename__ = 'chat'
    id = Column(String(255), primary_key=True, nullable=False)
    model = Column(String(255), nullable=False)
    object = Column(String(255), nullable=False)
    created = Column(String(255), nullable=False)
    finish_reason = Column(String(255), nullable=False)
    index = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    role = Column(String(255), nullable=False)
    completion_tokens = Column(String(255), nullable=False)
    prompt_tokens = Column(String(255), nullable=False)
    total_tokens = Column(String(255), nullable=False)
    session = Column(String(255), nullable=False)
    create_time = Column(DATETIME, nullable=False)


# 创建表结构，如果已存在则忽略
Base.metadata.create_all(engine)
# 创建一个会话对象，用于插入数据
session = Session()


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
        chat_obj.session = utils.session_utils.get_session_value()
        timestamp = datetime.fromtimestamp(time.time())
        chat_obj.create_time = timestamp
        # 将chat对象添加到会话中
        return chat_obj


def get_chat_obj_by_session(session_value):
    """
    获取数据库中相同session的对话内容
    :param session_value:
    :return:
    """
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
