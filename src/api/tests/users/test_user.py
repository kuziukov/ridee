from aiohttp.test_utils import unittest_run_loop
from api.service.session.jwt import JWTToken
from api.service.session.session import UserSession
from api.tests import AppTestCase


class UserTestCase(AppTestCase):
    @unittest_run_loop
    async def test_user_get(self):
        number = '+12345678900'
        user = {
            'phone': number,
            'region_code': 'RU',
            'blocked': False,
        }
        response = await self.app.db.users.insert_one(user)
        user['_id'] = response.inserted_id
        session = await UserSession(self.app).create_session(user)
        access_token, expires_in = JWTToken().generate(session)

        headers = {
            'Content-Type': 'application/json',
            'Token': access_token.decode("utf-8"),
        }
        response = await self.client.get("/v1.0/user", headers=headers)
        data = await response.json()
        assert data['code'] == 200
        assert data['status'] == 'success'
        result = data['result']
        assert isinstance(result['phone'], str)
        assert isinstance(result['_id'], str)
        assert isinstance(result['region_code'], str)

