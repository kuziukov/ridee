import phonenumbers
from phonenumbers import region_code_for_country_code
from pymongo.errors import DuplicateKeyError
from api.resources.authorization.schemas import (
    SerializationNumberCompleteSchema,
    DeserializationNumberCompleteSchema
)
from api.service.session.authorization import AuthorizationSession
from api.service.session.jwt import JWTToken
from api.service.session.session import UserSession
from cores.rest_core import (
    codes,
    APIException
)
from utils import (
    coordinates_from_region_code
)


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
                lat, long = coordinates_from_region_code(region_code)
                user = {
                    'phone': data['number'],
                    'region_code': region_code,
                    'blocked': False,
                    'last_coord': {
                        'lat': lat,
                        'long': long
                    }
                }

                try:
                    response = await request.app.db.users.insert_one(user)
                    user['_id'] = response.inserted_id
                except DuplicateKeyError:
                    raise AuthorizationCompleteException()

            session = await UserSession(request.app).create_session(user)
            access_token, expires_in = JWTToken().generate(session)
            result = {
                'access_token': access_token,
                'expires_in': expires_in
            }
            return SerializationNumberCompleteSchema().serialize(result)

    raise AuthorizationCompleteException()


