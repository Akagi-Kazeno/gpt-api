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


# 定义一个gpt_image类，对应于gpt_image表
class GptImage(Base):
    __tablename__ = 'gpt_image'
    id = Column(String(255), primary_key=True, nullable=False)
    created = Column(String(255), nullable=False)
    b64_image = Column(Text, nullable=False)
    session = Column(String(255), nullable=False)
    create_time = Column(DATETIME, nullable=False)


# 创建表结构，如果已存在则忽略
Base.metadata.create_all(engine)
# 创建一个会话对象，用于插入数据
session = Session()


def gpt_image_json_to_db(json_data):
    """
    处理gpt生成图片返回的json并返回数据库
    :param json_data:
    :return:
    """
    for data in json_data['data']:
        gpt_image_obj = GptImage()
        gpt_image_obj.id = utils.id_utils.simple_uuid()
        gpt_image_obj.created = json_data['created']
        gpt_image_obj.b64_image = data['b64_json']
        gpt_image_obj.session = utils.session_utils.get_session_value()
        timestamp = datetime.fromtimestamp(time.time())
        gpt_image_obj.create_time = timestamp
        # 将gpt_image_obj对象添加到会话中
        return gpt_image_obj


def get_gpt_image_by_session(session_value):
    """
    获取数据库中相同的session生成的image
    :param session_value:
    :return:
    """
    gpt_image_obj = session.query(GptImage.id).filter(GptImage.session == session_value).order_by(
        GptImage.create_time).all()
    return gpt_image_obj


def count_gpt_image_by_session(session_value):
    """
    计算数据库中相同session生成的image数量
    :param session_value:
    :return:
    """
    count_gpt_image: int = len(get_gpt_image_by_session(session_value))
    return count_gpt_image
