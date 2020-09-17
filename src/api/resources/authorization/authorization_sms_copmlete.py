import phonenumbers
from phonenumbers import region_code_for_country_code
from pymongo.errors import DuplicateKeyError

from api.resources.authorization.schemas import (
    SerializationNumberCompleteSchema,
    DeserializationNumberCompleteSchema
)
from api.service.session.authorization import AuthorizationSession
from api.service.session.jwt import Token
from api.service.session.session import create_session
from cores.rest_core import codes, APIException


class AuthorizationCompleteException(APIException):

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

            phone_number = phonenumbers.parse(data['number'], None, _check_region=True)
            region_code = region_code_for_country_code(phone_number.country_code)

            user = await request.app.db.users.find_one({'phone': data['number']})
            if user is None:

                user = {
                    'phone': data['number'],
                    'region_code': region_code,
                    'blocked': False,
                }

                try:
                    user = await request.app.db.users.insert_one(user)
                except DuplicateKeyError:
                    raise AuthorizationCompleteException()

            expires_in = 2629744
            session = await create_session(users=user, expires_in=expires_in, app=request.app)
            access_token, expires_in = Token(session_id=session.key, user_id=user['_id']).generate(expires_in)

            result = {
                'access_token': access_token,
                'expires_in': expires_in
            }
            return SerializationNumberCompleteSchema().serialize(result)

    raise AuthorizationCompleteException()

