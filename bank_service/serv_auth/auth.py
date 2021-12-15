from jwt import encode as encodeJWT, decode as decodeJWT

import functools
import io
import time
import jwt

import bot_service.service.util.validate as validator
import serv_auth.models as models

from bot_service.service.util.resp import fail, success, expire

from typing import Callable

from django.http.request import HttpRequest
from django.http.response import JsonResponse

from bank_service.settings import JWT_EXPIRE_IN, JWT_PUBLIC_PATH, JWT_SECRET_PATH


with io.open(JWT_SECRET_PATH, 'rb') as key:
    JWT_SECRET = key.read()
with io.open(JWT_PUBLIC_PATH, 'rb') as pub:
    JWT_PUBLIC = pub.read()


class ExposeAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Access-Control-Expose-Headers'] = "Authorization"
        return response


# 生成token
def generateToken(
    userId: int = None,
    name: str = None,
    detail: dict = None,
    payload: dict = None
) -> str:
    if payload is not None:
        token = encodeJWT(
            payload,
            JWT_SECRET, algorithm="RS256")
    else:
        token = encodeJWT({
            'id': userId,
            'name': name,
            'exp': int(time.time()) + JWT_EXPIRE_IN,
            'detail': detail
        }, JWT_SECRET, algorithm="RS256")
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


# 装饰器 更新token 检测过期并重定向
def preprocessToken(requestHandler: Callable) -> Callable:
    @functools.wraps(requestHandler)
    def wrapper(request: HttpRequest):
        # update token here
        token = request.META.get('HTTP_AUTHORIZATION')
        if token is None:
            return JsonResponse({
                'code': 50008,
                'msg': 'need login'
            })
        try:
            try:
                payload = decodeJWT(token, JWT_PUBLIC, algorithms=['RS256'])
                payload['exp'] = int(time.time()) + JWT_EXPIRE_IN
                token = generateToken(payload=payload)
            except jwt.ExpiredSignatureError:
                return JsonResponse({
                    'code': 50014,
                    'msg': 'token expired'
                })
            except jwt.DecodeError:
                return JsonResponse({
                    'code': 50008,
                    'msg': 'token broken'
                })
        except Exception as e:
            print(e)
            return JsonResponse({
                'code': 0,
                'message': 'error occured while handling token'
            })
        response: JsonResponse = requestHandler(request)
        response['Authorization'] = token
        return response
    return wrapper


sign_schema = {
    'type': 'object',
    'required': ['username', 'pwd'],
    'properties': {
        'username': {'type': 'string', 'minLength': 4, 'maxLength': 32, 'pattern': r'[a-z0-9A-Z_]+'},
        'pwd': {'type': 'string', 'length': 32}
    }
}


def sign(request: HttpRequest):
    stat, res = validator.validate(request, sign_schema)
    if stat == validator.FAIL:
        return JsonResponse(res)
    
    res['username'].lower()
    
    reg = False
    
    try:
        user = models.User.objects.get(name=res['username'])
    except models.User.DoesNotExist:
        reg = True
    
    if reg:
        user = models.User()
        user.name = res['username']
        user.pwd = res['pwd']
        user.save()
        
        token = generateToken(user.id, res['username'])
    else:
        user: models.User
        if user.pwd != res['pwd']:
            return JsonResponse(fail('wrong password.'))
        token = generateToken(user.id, res['username'])
    
    resp = JsonResponse(success())
    resp['Authorization'] = token
    return resp    
