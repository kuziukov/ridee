import jwt
import json
from bson import ObjectId
from aiohttp import web

from api.service.session.jwt import JWTToken
from cores.rest_core import (
    codes,
    APIException
)


class ApiKeyException(APIException):

    @property
    def message(self):
        return 'API key expired. Please renew the API key.'

    code = codes.BAD_REQUEST


class BlockingException(APIException):

    @property
    def message(self):
        return 'Your account is blocked!'

    code = codes.BAD_REQUEST


def token_required(func):
    async def wrapped(request):
        request.user = None
        jwt_token = request.headers.get('Token', None)

        try:
            payload = JWTToken().parse(jwt_token)
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            raise ApiKeyException()

        data = json.loads(await request.app.session.get(payload['id']))

        if data is None:
            raise ApiKeyException()
        elif payload['user_id'] != data['user_id']:
            raise ApiKeyException()

        user = await request.app.db.users.find_one({'_id': ObjectId(data['user_id'])})
        if user is None:
            raise ApiKeyException()
        elif 'blocked' not in user:
            raise BlockingException()
        elif user['blocked'] is True:
            raise BlockingException()

        request.user = user
        return await func(request)
    return wrapped
