import os
import time
from datetime import datetime

from dotenv import load_dotenv
# 导入sqlalchemy模块
from sqlalchemy import create_engine, Column, String, Text, DATETIME
from sqlalchemy.orm import sessionmaker, declarative_base

import utils.id_utils
import utils.session_utils

load_dotenv()

# 创建一个数据库引擎，连接到gpt数据库
engine = create_engine(os.getenv("DATABASE_URL"))
# 创建一个基类，用于定义表结构
Base = declarative_base()
# 创建一个会话类，用于操作数据库
Session = sessionmaker(bind=engine)


# 定义一个UserChat类，对应于user_chat表
class UserChatCompletion(Base):
    __tablename__ = 'user_chat_completion'
    id = Column(String(255), primary_key=True, nullable=False)
    session = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    create_time = Column(DATETIME, nullable=False)


# 创建表结构，如果已存在则忽略
Base.metadata.create_all(engine)
# 创建一个会话对象，用于插入数据
session = Session()


def user_chat_completion_to_db(message):
    """
    将用户的聊天输入插入数据库
    :param message:
    :return:
    """
    user_chat_obj = UserChatCompletion()
    user_chat_obj.id = utils.id_utils.simple_uuid()
    user_chat_obj.session = utils.session_utils.get_session_value()
    user_chat_obj.message = message
    timestamp = datetime.fromtimestamp(time.time())
    user_chat_obj.create_time = timestamp
    return user_chat_obj


def get_user_chat_completion_by_session(session_value):
    """
    获取数据库中相同session的用户对话
    :param session_value:
    :return:
    """
    user_chat_obj = session.query(UserChatCompletion.message).filter(
        UserChatCompletion.session == session_value).order_by(UserChatCompletion.create_time).all()
    return user_chat_obj


def count_user_chat_completion_by_session(session_value):
    """
    计算数据库中相同session的用户对话数量
    :param session_value:
    :return:
    """
    user_chat_count: int = len(get_user_chat_completion_by_session(session_value))
    return user_chat_count
