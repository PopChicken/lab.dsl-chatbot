import json
import bot_service.service.util.resp as resp
import jsonschema

from jsonschema import ValidationError

from json.decoder import JSONDecodeError
from typing import Any, Tuple
from enum import Enum

from django.http.request import HttpRequest


FAIL = 0
SUCCESS = 1


def validate(http_req: HttpRequest, schema: object) -> Tuple[bool, dict]:
    try:
        req = json.loads(http_req.body)
        jsonschema.validate(req, schema=schema)
    except JSONDecodeError:
        return FAIL, resp.fail("bad json format")
    except ValidationError as e:
        return FAIL, resp.fail(f"bad request body: {e.message}")
    return SUCCESS, req
