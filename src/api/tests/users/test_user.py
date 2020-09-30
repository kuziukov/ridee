import json

from aiohttp.test_utils import unittest_run_loop

from api.service.session.authorization import AuthorizationSession
from api.tests import AppTestCase


class UserTestCase(AppTestCase):
    @unittest_run_loop
    async def test_user_get(self):
        number = '+12345678900'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'number': number
        }
        response = await self.client.post("/v1.0/authorization/sms", data=json.dumps(data), headers=headers)
        data = await response.json()
        result = data['result']
        verify_key = result['verify_key']

        session = AuthorizationSession(number, app=self.app)
        result, expires_in = await session.get_data()
        sms_code = result['sms_code']

        response = await self.client.post("/v1.0/authorization/sms/complete", data=json.dumps({
            'number': number,
            'verify_key': verify_key,
            'sms_code': sms_code,
        }), headers=headers)
        data = await response.json()
        result = data['result']
        access_token = result['access_token']

        headers['Token'] = access_token
        response = await self.client.get("/v1.0/user", headers=headers)
        data = await response.json()
        assert data['code'] == 200
        assert data['status'] == 'success'
        result = data['result']
        assert isinstance(result['phone'], str)
        assert isinstance(result['_id'], str)
        assert isinstance(result['region_code'], str)


