import time

from flask import session, request


def create_session_id():
    """
    创建session_id
    :return:
    """
    if 'session_id' not in session:
        session['session_id'] = str(time.time())
        print(session)
    return session


def get_session_id():
    """
    获取session_id
    :return:
    """
    session_id = session.get('session_id')
    return session_id


def get_session_value():
    """
    获取session的值
    :return:
    """
    session_value = request.cookies.get('session')
    return session_value


def delete_session():
    """
    删除session
    :return:
    """
    if 'session_id' in session:
        session.pop('session_id')
