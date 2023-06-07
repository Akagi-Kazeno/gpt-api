# 导入sqlalchemy模块
from sqlalchemy import Column, String, Text, DATETIME, Boolean,JSON

from entity.db_init import get_db_session, get_db_base, create_db_engine

# 创建一个数据库引擎，连接到数据库
engine = create_db_engine()
# 创建一个基类，用于定义表结构
Base = get_db_base()
# 创建一个会话类，用于操作数据库
Session = get_db_session()


class WebChatResponseEntity(Base):
    __tablename__ = 'web_chat_response'
    web_chat_id = Column(String(255), primary_key=True, nullable=False)
    chat_metadata = Column(JSON, nullable=True)
    name = Column(Text, nullable=True)
    role = Column(String(255), nullable=True)
    citations = Column(JSON, nullable=True)
    conversation_id = Column(String(255), nullable=False)
    end_turn = Column(Boolean, nullable=False)
    finish_details = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    model = Column(String(255), nullable=False)
    parent_id = Column(String(255), nullable=False)
    recipient = Column(String(255), nullable=False)
    session = Column(String(255), nullable=False)
    create_time = Column(DATETIME, nullable=False)


def create_table():
    # 创建表结构，如果已存在则忽略
    create_table = Base.chat_metadata.create_all(engine)
    return create_table


def create_session():
    # 创建一个会话对象，用于插入数据
    session = Session()
    return session
