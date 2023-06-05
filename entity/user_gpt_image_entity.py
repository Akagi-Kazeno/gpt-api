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


# 定义一个UserGptImage类，对应于user_gpt_image表
class UserGptImage(Base):
    __tablename__ = 'user_gpt_image'
    id = Column(String(255), primary_key=True, nullable=False)
    session = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    create_time = Column(DATETIME, nullable=False)


# 创建表结构，如果已存在则忽略
Base.metadata.create_all(engine)
# 创建一个会话对象，用于插入数据
session = Session()


def user_gpt_image_to_db(description: str):
    """
    将用户的图片描述输入插入数据库
    :param description:
    :return:
    """
    user_gpt_image_obj = UserGptImage()
    user_gpt_image_obj.id = utils.id_utils.simple_uuid()
    user_gpt_image_obj.session = utils.session_utils.get_session_value()
    user_gpt_image_obj.description = description
    timestamp = datetime.fromtimestamp(time.time())
    user_gpt_image_obj.create_time = timestamp
    return user_gpt_image_obj


def get_user_gpt_image_by_session(session_value):
    """
    获取数据库中相同session的图片描述
    :param session_value:
    :return:
    """
    gpt_image_obj = session.query(UserGptImage.description).filter(UserGptImage.session == session_value).order_by(
        UserGptImage.create_time).all()
    return gpt_image_obj


def count_user_gpt_image_by_session(session_value):
    """
    计算数据库中相同session的图片描述
    :param session_value:
    :return:
    """
    gpt_image_count: int = len(get_user_gpt_image_by_session(session_value))
    return gpt_image_count
