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
# import threading
# import uuid
import bank_service.settings as settings
from bot_service.service.model.exception import ServiceException

import bot_service.service.model.loader as loader

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


def init(session: SessionBase, req: dict) -> list:
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
    schema = req['schema']
    if schema not in loader.bots:
        raise ServiceException("unknown schema")
    
    session['schema'] = schema
    session['status'] = 0
    
    bot = loader.bots[schema]
    # if key not in session_locks:
    #     lock = threading.RLock()
    #     session_locks[key] = lock
    # else:
    #     lock = session_locks[key]
    
    # crontab.add(key, settings.SESSION_COOKIE_AGE, on_expire, (key, ))
    
    try:
        # lock.acquire()
        _, reps = bot.handle_message(0, None)
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
    
    schema = session.get('schema')
    stat = session.get('status')

    if schema is None or stat is None:
        raise ServiceException("illegal access")
    
    if schema not in loader.bots:
        raise ServiceException("non-existed schema")
    
    bot = loader.bots[schema]

    try:
        # lock.acquire()
        stat, reps = bot.handle_message(stat, msg)
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