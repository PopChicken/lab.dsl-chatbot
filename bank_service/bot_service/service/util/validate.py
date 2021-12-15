"""the module to check whether a request is legal

Powered by JSONSchema, this module allows developers
separate controller and service. The process changed
from all-by-controller to controller verifying, service
handling and controller send back.

Typical usage:
from bot_service.service.util.resp import fail, success, expire


message_schema = {
    'type': 'object',
    'required': [],
    'properties': {
        'content': {'type': 'string'}
    }
}

stat, res = validator.validate(request, message_schema)
if stat == validator.FAIL:
    return JsonResponse(res)

try:
    resp = data.service(request.session, res)
except Exception as e:
    return JsonResponse(fail(str(e)))

return JsonResponse(success(resp))
"""
import json
import bot_service.service.util.resp as resp
import jsonschema

from jsonschema import ValidationError

from json.decoder import JSONDecodeError
from typing import Tuple

from django.http.request import HttpRequest


FAIL = False
SUCCESS = True


def validate(http_req: HttpRequest, schema: object) -> Tuple[bool, dict]:
    """validate a request with a schema

    Args:
        http_req (HttpRequest): an user http request
        schema (object): a json schema matches the wanted request

    Returns:
        Tuple[bool, dict]: (status, a verified request dict or failing response)
    """
    try:
        req = json.loads(http_req.body)
        jsonschema.validate(req, schema=schema)
    except JSONDecodeError:
        return FAIL, resp.fail("bad json format")
    except ValidationError as e:
        return FAIL, resp.fail(f"bad request body: {e.message}")
    return SUCCESS, req
