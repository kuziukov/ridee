import jwt
from api.resources.oauth.oauth_code_post import SerializationSchema
from api.resources.session.schemas import DeserializationRefreshSchema
from api.service import Session
from api.service.session import (
    JWTToken,
    create_tokens
)
from cores.rest_core import (
    APIException,
    codes
)
from models import Users


class RefreshTokenException(APIException):

    @property
    def message(self):
        return 'Refresh token expired. Please sign in again.'

    code = codes.REFRESH_TOKEN_EXPIRED


async def SessionPost(request):
    app = request.app
    data = DeserializationRefreshSchema().deserialize(await request.json())
    try:
        payload = JWTToken().parse(data['refresh_token'])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        raise RefreshTokenException()

    session_id = f'{payload["user_id"]}:{payload["id"]}'
    session = Session(request.app, session_id)
    if not await session.is_exists():
        raise RefreshTokenException()

    data, _ = await session.get_data()
    if not data:
        raise RefreshTokenException()
    elif payload['user_id'] != data['user_id']:
        raise RefreshTokenException()

    if 'refresh_key' not in payload:
        raise RefreshTokenException()
    elif payload['refresh_key'] != data['refresh_key']:
        raise RefreshTokenException()

    user = await Users.find_one({'_id': data['user_id']})
    if not user:
        raise RefreshTokenException()
    await session.destroy()

    response = await create_tokens(app=app,
                             user=user)
    return SerializationSchema().serialize(response)
