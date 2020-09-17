import jwt
import json
import config
from bson import ObjectId
from aiohttp import web
from cores.rest_core import (
    codes,
    APIException
)


class ApiKeyException(APIException):

    @property
    def message(self):
        return 'API key expired. Please renew the API key.'

    code = codes.BAD_REQUEST


class ProfileInformationException(APIException):

    @property
    def message(self):
        return 'Your name or surname is not filled. Please fill the information before.'

    code = codes.BAD_REQUEST


class BlockingException(APIException):

    @property
    def message(self):
        return 'Your account is blocked!'

    code = codes.BAD_REQUEST


def login_required(func):
    async def wrapped(request):
        request.user = None

        jwt_token = request.headers.get('Token', None)
        if jwt_token is None:
            raise web.HTTPUnauthorized()
        try:
            payload = jwt.decode(jwt_token, config.SECRET_KEY, algorithms=['HS256'])
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
        elif 'name' not in user or 'surname' not in user or 'blocked' not in user:
            raise ProfileInformationException()
        elif user['blocked'] is True:
            raise BlockingException()
        elif user['name'] is None or user['surname'] is None:
            raise ProfileInformationException()

        request.user = user
        return await func(request)
    return wrapped
