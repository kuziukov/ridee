import phonenumbers
from phonenumbers import region_code_for_country_code
from api.resources.authorization.schemas import (
    SerializationNumberCompleteSchema,
    DeserializationNumberCompleteSchema
)
from api.service import AuthorizationSession
from api.service.session import (
    UserSession,
    JWTToken
)
from cores.rest_core import (
    codes,
    APIException
)
from models import Users
from models.users import LastCoordinates
from utils import (
    coordinates_from_region_code
)


class ExpiredException(APIException):

    @property
    def message(self):
        return 'Authentication time has expired. Please start again from the launcher.'

    code = codes.BAD_REQUEST


class SMSCodeException(APIException):

    @property
    def message(self):
        return 'SMS Verification Code is Invalid.'

    code = codes.BAD_REQUEST


async def AuthorizationSmsCompletePost(request):

    data = DeserializationNumberCompleteSchema().deserialize(await request.json())
    session = AuthorizationSession(data['number'], app=request.app)

    if not await session.is_exists():
        raise ExpiredException()

    result, expires_in = await session.get_data()
    if result['verify_key'] != data['verify_key'] or result['sms_code'] != data['sms_code']:
        raise SMSCodeException()

    await session.destroy()
    phone_number = phonenumbers.parse(data['number'], None, _check_region=True)
    region_code = region_code_for_country_code(phone_number.country_code)

    user = await Users.find_one({'phone': data['number']})
    if user is None:
        lat, long = coordinates_from_region_code(region_code)

        user = Users()
        user.phone = data['number']
        user.region_code = region_code
        user.blocked = False
        user.last_coord = LastCoordinates()
        user.last_coord.lat = lat
        user.last_coord.long = long

        try:
            await user.commit()
        except Exception as e:
            raise ExpiredException()

    session = await UserSession(request.app).create_session(user)
    access_token, expires_in = JWTToken().generate_access(session)
    refresh_token, refresh_expires_in = JWTToken().generate_refresh(session)
    result = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': expires_in
    }
    return SerializationNumberCompleteSchema().serialize(result)

