def fail(msg: str) -> dict:
    resp = {
        'code': 1,
        'msg': msg,
        'data': None
    }
    return resp


def expire(msg: str) -> dict:
    resp = {
        'code': 2,
        'msg': msg,
        'data': None
    }
    return resp


def success(resp_body: dict | list=None) -> dict:
    resp = {
        'code': 0,
        'msg': "success",
        'data': resp_body
    }
    return resp