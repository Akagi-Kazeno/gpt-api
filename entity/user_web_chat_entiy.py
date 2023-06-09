from sqlalchemy import Column, String, Text, DATETIME

from entity.db_init import get_db_session, get_db_base, create_db_engine

engine = create_db_engine()
Base = get_db_base()
Session = get_db_session()


class UserWebChat(Base):
    __tablename__ = "user_web_chat"
    id = Column(String(255), primary_key=True, nullable=False)
    message = Column(Text, nullable=False)
    session = Column(String(255), nullable=False)
    create_time = Column(DATETIME, nullable=False)


def create_table():
    create_table = Base.create_all(engine)
    return create_table


def create_session():
    session = Session()
    return session
