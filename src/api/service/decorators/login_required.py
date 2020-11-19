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

    code = codes.UNAUTHORIZED


class InformationException(APIException):

    @property
    def message(self):
        return 'Your name or surname is not filled. Please fill the information before.'

    code = codes.FORBIDDEN


class BlockingException(APIException):

    @property
    def message(self):
        return 'Your account is blocked!'

    code = codes.FORBIDDEN


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
                session_id = f'{str(payload["user_id"])}:{payload["id"]}'
                data = json.loads(await request.app.session.get(session_id))
            except Exception:
                raise ApiKeyException()

            if not data:
                raise ApiKeyException()
            elif 'refresh_key' in payload:
                raise ApiKeyException()
            elif payload['user_id'] != data['user_id']:
                raise ApiKeyException()

            user = await Users.find_one({'_id': ObjectId(data['user_id'])})
            if not user:
                raise ApiKeyException()
            elif user.blocked:
                raise BlockingException()
            elif not skip_info and (not user.name or not user.surname):
                raise InformationException()

            request.user = user
            return await func(request)
        return wrapped_f
    return wrapped
