import jwt
from api.resources.authorization.schemas import (
    SerializationNumberCompleteSchema
)
from api.resources.session.schemas import DeserializationRefreshSchema
from api.service import Session
from api.service.session import (
    JWTToken,
    UserSession
)
from cores.rest_core import (
    APIException,
    codes
)
from models import Users


class RefreshKeyException(APIException):

    @property
    def message(self):
        return 'Refresh token expired. Please sign in again.'

    code = codes.BAD_REQUEST


async def SessionPost(request):

    data = DeserializationRefreshSchema().deserialize(await request.json())
    try:
        payload = JWTToken().parse(data['refresh_token'])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        raise RefreshKeyException()

    session_id = f'{payload["user_id"]}:{payload["id"]}'
    session = Session(request.app, session_id)
    
    if not await session.is_exists():
        raise RefreshKeyException()

    data, _ = await session.get_data()
    if not data:
        raise RefreshKeyException()
    elif payload['user_id'] != data['user_id']:
        raise RefreshKeyException()

    if 'refresh_key' not in payload:
        raise RefreshKeyException()
    elif payload['refresh_key'] != data['refresh_key']:
        raise RefreshKeyException()

    user = await Users.find_one({'_id': data['user_id']})
    if user is None:
        raise RefreshKeyException()
    await session.destroy()

    session = await UserSession(request.app).create_session(user)
    access_token, expires_in = JWTToken().generate_access(session)
    refresh_token, refresh_expires_in = JWTToken().generate_refresh(session)
    result = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': expires_in
    }
    return SerializationNumberCompleteSchema().serialize(result)

