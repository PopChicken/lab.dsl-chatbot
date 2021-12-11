"""a simple module to generate specified response
"""
def fail(msg: str) -> dict:
    """when a request's response fails to make, use this

    Args:
        msg (str): message to describe details of the failure

    Returns:
        dict: the response
    """
    resp = {
        'code': 1,
        'msg': msg,
        'data': None
    }
    return resp


def expire(msg: str) -> dict:
    """DEPRECATED. when something like session expired, use this.

    Args:
        msg (str): message to describe details of the expiration

    Returns:
        dict: the response
    """
    resp = {
        'code': 2,
        'msg': msg,
        'data': None
    }
    return resp


def success(resp_body: dict | list=None) -> dict:
    """to generate the success response

    Args:
        resp_body (dict, optional): the data in response. can be a dict
        or list. Defaults to None.

    Returns:
        dict: the response
    """
    resp = {
        'code': 0,
        'msg': "success",
        'data': resp_body
    }
    return resp