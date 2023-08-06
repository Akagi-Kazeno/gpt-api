import time

from flask import session, request


def create_session_time_stamp():
    """
    创建session_id
    :return:
    """
    if 'time_stamp' not in session:
        session['time_stamp'] = str(time.time())
    return session


def get_session_time_stamp():
    """
    获取session_id
    :return:
    """
    session_id = session.get('time_stamp')
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


def create_new_session():
    """
    创建新的session
    """
    session_value = request.cookies.get('session')
    if session_value is None:
        create_session_time_stamp()
        session_value = request.cookies.get('session')
    return session_value


def create_wx_session(wxid: str):
    """
    创建微信session
    """
    session['wxid'] = wxid
    return session
