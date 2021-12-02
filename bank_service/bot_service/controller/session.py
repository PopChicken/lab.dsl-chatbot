"""
this module provides the interfaces of session

"""
import time
import threading
import jsonschema

import bot_service.service.data.session as data
import bot_service.service.util.validate as validator

from bot_service.service.util.resp import fail, success, expire

from django.http.request import HttpRequest
from django.http.response import JsonResponse


message_schema = {
    'type': 'object',
    'required': [],
    'properties': {
        'content': {'type': 'string'}
    }
}


def init(request: HttpRequest) -> JsonResponse:
    try:
        resp = data.init(request.session)
    except Exception as e:
        return JsonResponse(fail(str(e)))
    return JsonResponse(success(resp))


def message(request: HttpRequest) -> JsonResponse:
    stat, res = validator.validate(request, message_schema)
    if stat == validator.FAIL:
        return JsonResponse(res)

    try:
        resp = data.message(request.session, res)
    except TimeoutError as e:
        return JsonResponse(expire(str(e)))
    except Exception as e:
        return JsonResponse(fail(str(e)))

    return JsonResponse(success(resp))