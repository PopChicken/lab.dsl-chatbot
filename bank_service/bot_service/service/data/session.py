"""this module provides the implementations of session api

Separeted service module. It will handling the verified user
requests passed from controllers. The verified request is a 
legal dict object, which means the function inside this module
do not need any verification to see if the input is illegal.

Typical usage example:
try:
    resp = data.func(request)
except Exception as e:
    return JsonResponse(fail(str(e)))
return JsonResponse(success(resp))

"""
import time
import threading
import uuid
import bank_service.settings as settings

import bot_service.service.model.manager as manager

from bot_service.service.util.crontab import Crontab

from django.contrib.sessions.backends.base import SessionBase


# session_locks = {}
# 
# crontab = Crontab()
# 
# 
# def on_expire(key: str):
#     if key in session_locks:
#         del session_locks[key]


def init(session: SessionBase) -> list:
    """init a session (probably re-init)

    Args:
        session (SessionBase): a user session

    Raises:
        Exception: the exception during generating welcome message

    Returns:
        list: message list
    """
    # key = session.get('key')
    # if key is None:
    #     session['key'] = str(uuid.uuid4())
    session['status'] = 0
    # if key not in session_locks:
    #     lock = threading.RLock()
    #     session_locks[key] = lock
    # else:
    #     lock = session_locks[key]
    
    # crontab.add(key, settings.SESSION_COOKIE_AGE, on_expire, (key, ))
    
    try:
        # lock.acquire()
        _, reps = manager.bot.handle_message(0, None)
        # lock.release()
    except Exception as e:
        # lock.release()
        raise e

    rep = []
    for r in reps:
        rep.append({
            'content': r,
            'time': round(time.time() * 1000)
        })
    return rep


def message(session: SessionBase, req: dict) -> list:
    """handle a messgae request

    Args:
        session (SessionBase): an user session
        req (dict): a verified user request

    Raises:
        Exception: the exception during generating message to reply

    Returns:
        list: message list
    """
    msg = req['content']
    # key = session.get('key')
    # lock: threading.RLock = session_locks.get(key)

    # if lock is None:
    #     raise TimeoutError("timeout")
    
    stat = session.get('status')

    if stat is None:
        raise Exception("illegal")

    try:
        # lock.acquire()
        stat, reps = manager.bot.handle_message(stat, msg)
        # lock.release()
    except Exception as e:
        # lock.release()
        raise e

    session['status'] = stat
    rep = []
    for r in reps:
        rep.append({
            'content': r,
            'time': round(time.time() * 1000)
        })
    return rep