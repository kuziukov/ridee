import phonenumbers
from phonenumbers import region_code_for_country_code
from api.service import OAuthSession
from api.service.session import (
    create_tokens
)
from cores.marshmallow_core import (
    ApiSchema,
    fields
)
from cores.rest_core import (
    codes,
    APIException
)
from models import (
    Users,
    LastCoordinates
)
from utils import (
    coordinates_from_region_code
)


class TimeExpiredException(APIException):

    @property
    def message(self):
        return 'Authentication time has expired.'

    code = codes.AUTHORIZATION_EXPIRED


class CodeException(APIException):

    @property
    def message(self):
        return 'Invalid verification code.'

    code = codes.BAD_REQUEST


class DeserializationSchema(ApiSchema):
    number = fields.PhoneNumber(required=True)
    verify_key = fields.Str(required=True)
    code = fields.Str(required=True)


class SerializationSchema(ApiSchema):
    access_token = fields.Str(default=None)
    refresh_token = fields.Str(default=None)
    expires_in = fields.Timestamp(default=None)


async def OAuthCodePost(request):
    app = request.app
    data = DeserializationSchema().deserialize(await request.json())
    session = OAuthSession(key=data['number'],
                           app=app)

    if not await session.is_exists():
        raise TimeExpiredException()

    result, expires_in = await session.get_data()
    if result['verify_key'] != data['verify_key'] or result['code'] != data['code']:
        raise CodeException()
    await session.destroy()

    phone_number = phonenumbers.parse(number=data['number'],
                                      _check_region=True)
    region_code = region_code_for_country_code(country_code=phone_number.country_code)

    user = await Users.find_one({'phone': data['number']})
    if user is None:
        user = Users()
        user.phone = data['number']
        user.region_code = region_code
        user.blocked = False
        user.last_coord = LastCoordinates()

        lat, long = coordinates_from_region_code(region_code)
        user.last_coord.lat = lat
        user.last_coord.long = long
        await user.commit()

    response = create_tokens(app=app,
                             user=user)
    return SerializationSchema().serialize(response)
