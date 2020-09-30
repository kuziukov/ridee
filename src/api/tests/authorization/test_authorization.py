import json
from aiohttp.test_utils import unittest_run_loop
from api.service.session.authorization import AuthorizationSession
from api.tests import AppTestCase
from utils import (
    generate_uuid1,
    generate_sms_code
)


class AuthorizationTestCase(AppTestCase):
    @unittest_run_loop
    async def test_authorization_post(self):
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'number': '+12345678900'
        }
        response = await self.client.post("/v1.0/authorization/sms", data=json.dumps(data), headers=headers)
        data = await response.json()
        assert data['code'] == 200
        assert data['status'] == 'success'
        result = data['result']
        assert result['expires_in'] <= 180
        assert isinstance(result['verify_key'], str)

    @unittest_run_loop
    async def test_authorization_complete_post(self):
        number = '+12345678900'
        session = AuthorizationSession(number, app=self.app)
        verify_key = generate_uuid1()
        sms_code = generate_sms_code()
        session.data = {
            "verify_key": verify_key,
            "sms_code": sms_code
        }
        await session.save()

        response = await self.client.post("/v1.0/authorization/sms/complete", data=json.dumps({
            'number': number,
            'verify_key': verify_key,
            'sms_code': sms_code,
        }))
        data = await response.json()
        assert data['code'] == 200
        assert data['status'] == 'success'
        result = data['result']
        assert isinstance(result['access_token'], str)
        assert isinstance(result['expires_in'], float)

