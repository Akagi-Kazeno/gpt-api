# https://github.com/Akagi-Kazeno/gpt-api-frontend/blob/master/package.json
# https://github.com/Akagi-Kazeno/gpt-api-frontend/blob/master/package.jsonhttps://github.com/Akagi-Kazeno/gpt-api-frontend/blob/master/package.json
import os

from dotenv import load_dotenv
# 导入sqlalchemy模块
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()


def create_db_engine():
    # 创建一个数据库引擎，连接到数据库
    engine = create_engine(os.getenv("DATABASE_URL"))
    return engine


def get_db_session():
    engine = create_db_engine()
    # 创建一个会话类，用于操作数据库
    Session = sessionmaker(bind=engine)
    return Session


def get_db_base():
    # 创建一个基类，用于定义表结构
    Base = declarative_base()
    return Base
