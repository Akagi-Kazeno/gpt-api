# 导入sqlalchemy模块
from sqlalchemy import Column, String, DATETIME

from db_init import get_db_session, get_db_base, create_db_engine

# 创建一个数据库引擎，连接到数据库
engine = create_db_engine()
# 创建一个基类，用于定义表结构
Base = get_db_base()
# 创建一个会话类，用于操作数据库
Session = get_db_session()


# 定义一个user类，对应于user表
class User(Base):
    __tablename__ = 'user'
    user_id = Column(String(255), primary_key=True, nullable=False)
    user_name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    create_time = Column(DATETIME, nullable=False)
    update_time = Column(DATETIME)
    last_login_time = Column(DATETIME)
    last_login_ip = Column(String(255))
    is_delete = Column(String(255), nullable=False)


def create_table():
    # 创建表结构，如果已存在则忽略
    create_table = Base.metadata.create_all(engine)
    return create_table


def create_session():
    # 创建一个会话对象，用于插入数据
    session = Session()
    return session
