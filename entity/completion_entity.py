# 导入sqlalchemy模块
from sqlalchemy import Column, String, Text, DATETIME

from db_init import get_db_session, get_db_base, create_db_engine

# 创建一个数据库引擎，连接到数据库
engine = create_db_engine()
# 创建一个基类，用于定义表结构
Base = get_db_base()
# 创建一个会话类，用于操作数据库
Session = get_db_session()


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


def create_table():
    # 创建表结构，如果已存在则忽略
    create_table = Base.metadata.create_all(engine)
    return create_table


def create_session():
    # 创建一个会话对象，用于插入数据
    session = Session()
    return session
