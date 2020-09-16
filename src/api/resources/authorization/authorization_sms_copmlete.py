from api.resources.authorization.schemas import (
    SerializationNumberCompleteSchema,
    DeserializationNumberCompleteSchema
)
from api.service.session.authorization import AuthorizationSession
from api.service.session.jwt import Token
from api.service.session.session import Session, create_session
from cores.rest_core import codes, APIException


class CommunityException(APIException):

    @property
    def message(self):
        return 'The authorization is not completed, please check the data'

    code = codes.BAD_REQUEST


async def AuthorizationSmsCompletePost(request):

    data = DeserializationNumberCompleteSchema().deserialize(await request.json())

    session = AuthorizationSession(data['number'], app=request.app)
    if await session.is_exists():
        result, expires_in = await session.get_data()
        if (result['verify_key'] == data['verify_key']) and \
                (result['sms_code'] == data['sms_code']):
            await session.destroy()

            expires_in = 2629744
            users = {'id': '12345'}
            #session = create_session(users=users, expires_in=expires_in, app=request.app)
            access_token, expires_in = Token(session_id=users['id'], user_id=users['id']).generate(expires_in)

            result = {
                'access_token': access_token,
                'expires_in': expires_in
            }
            return SerializationNumberCompleteSchema().serialize(result)

    raise CommunityException()

