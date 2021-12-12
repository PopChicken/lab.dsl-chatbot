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

import bot_service.service.model.loader as loader

from django.contrib.sessions.backends.base import SessionBase


def option() -> list:
    """show all the options

    Args:
        session (SessionBase): a user session

    Returns:
        list: option list
    """

    rep = []
    for schema_id, bot in loader.bots.items():
        settings = bot.get_settings()
        title = settings['title']
        rep.append({
            'schema': schema_id,
            'title': title
        })
    return rep


def detail(req: dict) -> dict:
    """get detail of specified schema

    Args:
        session (SessionBase): a user session

    Returns:
        list: detail
    """
    bot = loader.bots.get(req['schema'])
    if bot is None:
        return {}
    return bot.get_settings()