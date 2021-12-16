import unittest
import serv_auth.auth as auth
import base64
import jwt
import json

from django.http.request import HttpRequest
from django.http.response import JsonResponse

from bank_service.settings import JWT_PUBLIC_PATH


class TestAuth(unittest.TestCase):
    def test_generate(self):
        payload = {
            'teststr': 'hello world',
            'testnum': 100,
            'testbool': True,
            'testnull': None,
            'testlist': ['test'],
            'testdict': {
                'test': 'testdict'
            }
        }

        token = auth.generateToken(1, 'test_user', payload=payload)
        comps = token.split('.')
        payload_b64 = comps[1] + "=" * divmod(len(comps[1]), 4)[1]

        payload = json.loads(base64.urlsafe_b64decode(payload_b64))

        assert payload['teststr'] == 'hello world'
        assert payload['testnum'] == 100
        assert payload['testbool'] == True
        assert payload['testnull'] == None
        assert isinstance(payload['testlist'], list)
        assert len(payload['testlist']) == 1
        assert payload['testlist'][0] == 'test'
        assert payload['testdict']['test'] == 'testdict'

        with open(JWT_PUBLIC_PATH, 'r') as f:
            pub = f.read()
        
        payload = jwt.decode(token, pub, algorithms='RS256')

        assert payload['teststr'] == 'hello world'
        assert payload['testnum'] == 100
        assert payload['testbool'] == True
        assert payload['testnull'] == None
        assert isinstance(payload['testlist'], list)
        assert len(payload['testlist']) == 1
        assert payload['testlist'][0] == 'test'
        assert payload['testdict']['test'] == 'testdict'

    def test_expire(self):
        auth.JWT_EXPIRE_IN = -1
        token = auth.generateToken(1, 'test_user')
        
        with open(JWT_PUBLIC_PATH, 'r') as f:
            pub = f.read()

        expired = False
        try:
            jwt.decode(token, pub, algorithms='RS256')
        except jwt.ExpiredSignatureError:
            expired = True
        
        assert expired
    
    def test_preprocess(self):
        @auth.preprocessToken
        def http_handler(request: HttpRequest):
            pass

        auth.JWT_EXPIRE_IN = -1
        token = auth.generateToken(1, 'test_user')
        req = HttpRequest()
        req.META['HTTP_AUTHORIZATION'] = token
        
        resp: JsonResponse = http_handler(req)
        res = json.loads(resp.getvalue())
        assert res['code'] == 50014
        
        req = HttpRequest()
        req.META['HTTP_AUTHORIZATION'] = 'bad token'
        
        resp: JsonResponse = http_handler(req)
        res = json.loads(resp.getvalue())
        assert res['code'] == 50008
        
        req = HttpRequest()
        req.META['HTTP_AUTHORIZATION'] = None
        
        resp: JsonResponse = http_handler(req)
        res = json.loads(resp.getvalue())
        assert res['code'] == 50008