"""this module provides the interfaces of protal

Separeted controller module. It will handling the user requests
and make sure them verified. The verified requests will be packed
into dict then be sent to service layout. The benefit is extract
service operations from controllers easily and safely.

Typical usage example:
from django.urls import path

import portal


urlpatterns = [
    path('option', portal.option)
]
"""
import bot_service.service.data.portal as data
import bot_service.service.util.validate as validator

from bot_service.service.util.resp import fail, success, expire

from django.http.request import HttpRequest
from django.http.response import JsonResponse


detail_schema = {
    'type': 'object',
    'required': ['schema'],
    'properites': {
        'schema': {'type': 'string'}
    }
}


def option(request: HttpRequest) -> JsonResponse:
    """portal option api

    Args:
        request (HttpRequest): user request

    Returns:
        JsonResponse: response
    """
    try:
        resp = data.option()
    except Exception as e:
        return JsonResponse(fail(str(e)))
    return JsonResponse(success(resp))


def detail(request: HttpRequest) -> JsonResponse:
    """portal detail api

    return the detail of asked schema

    Args:
        request (HttpRequest): user request

    Returns:
        JsonResponse: response
    """
    stat, res = validator.validate(request, detail_schema)
    if stat == validator.FAIL:
        return JsonResponse(res)

    try:
        resp = data.detail(res)
    except Exception as e:
        return JsonResponse(fail(str(e)))

    return JsonResponse(success(resp))