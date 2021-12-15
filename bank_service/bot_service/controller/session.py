"""this module provides the interfaces of session

Separeted controller module. It will handling the user requests
and make sure them verified. The verified requests will be packed
into dict then be sent to service layout. The benefit is extract
service operations from controllers easily and safely.

Typical usage example:
from django.urls import path

import session


urlpatterns = [
    path('init', session.init),
    path('message', session.message)
]
"""
import bot_service.service.data.session as data
import bot_service.service.util.validate as validator
import serv_auth.auth as auth

from bot_service.service.util.resp import fail, success, expire

from django.http.request import HttpRequest
from django.http.response import JsonResponse


# json schema defines what init api wants
init_schema = {
    'type': 'object',
    'required': ['schema'],
    'properites': {
        'schema': {'type': 'string'}
    }
}

# json schema defines what message api wants
message_schema = {
    'type': 'object',
    'required': ['content'],
    'properties': {
        'content': {'type': 'string'}
    }
}


@auth.preprocessToken
def init(request: HttpRequest) -> JsonResponse:
    """session initialization api

    Args:
        request (HttpRequest): user request

    Returns:
        JsonResponse: response
    """
    stat, res = validator.validate(request, init_schema)
    if stat == validator.FAIL:
        return JsonResponse(res)

    try:
        resp = data.init(request.session, res)
    except Exception as e:
        return JsonResponse(fail(str(e)))
    return JsonResponse(success(resp))


@auth.preprocessToken
def message(request: HttpRequest) -> JsonResponse:
    """message handling api

    Args:
        request (HttpRequest): user request

    Returns:
        JsonResponse: response
    """
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