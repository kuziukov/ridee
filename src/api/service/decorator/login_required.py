import jwt
import json
from bson import ObjectId

from api.service.session.jwt import JWTToken
from cores.rest_core import (
    codes,
    APIException
)
from models.users import Users


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


def login_required(skip_info=False):
    def wrapped(func):
        async def wrapped_f(request):
            request.user = None
            jwt_token = request.headers.get('Token', None)

            try:
                payload = JWTToken().parse(jwt_token)
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                raise ApiKeyException()

            try:
                data = json.loads(await request.app.session.get(payload['id']))
            except Exception:
                raise ApiKeyException()

            if data is None:
                raise ApiKeyException()
            elif payload['user_id'] != data['user_id']:
                raise ApiKeyException()

            user = await Users.find_one({'_id': ObjectId(data['user_id'])})
            if user is None:
                raise ApiKeyException()
            elif user.blocked is True:
                raise BlockingException()
            elif not skip_info and (user.name is None or user.surname is None):
                raise ProfileInformationException()

            request.user = user
            return await func(request)
        return wrapped_f
    return wrapped
