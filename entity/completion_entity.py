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


# 定义一个completion类，对应于completion表
class Completion(Base):
    __tablename__ = 'completion'
    id = Column(String(255), primary_key=True, nullable=False)
    model = Column(String(255), nullable=False)
    object = Column(String(255), nullable=False)
    created = Column(String(255), nullable=False)
    finish_reason = Column(String(255), nullable=False)
    index = Column(String(255), nullable=False)
    logprobs = Column(Text, nullable=True)
    text = Column(Text, nullable=False)
    completion_tokens = Column(String(255), nullable=False)
    prompt_tokens = Column(String(255), nullable=False)
    total_tokens = Column(String(255), nullable=False)
    session = Column(String(255), nullable=False)
    create_time = Column(DATETIME, nullable=False)


# 创建表结构，如果已存在则忽略
Base.metadata.create_all(engine)
# 创建一个会话对象，用于插入数据
session = Session()


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
        completion_obj.session = utils.session_utils.get_session_value()
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
