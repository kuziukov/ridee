from api.service.session.oauth_session import OAuthSession
from cores.marshmallow_core import (
    ApiSchema,
    fields
)
from cores.rest_core import (
    APIException,
    codes
)
from utils import (
    generate_uuid1,
    generate_code
)


class CountyException(APIException):

    @property
    def message(self):
        return 'The service is not available in your country.'

    code = codes.FORBIDDEN


class DeserializationSchema(ApiSchema):
    number = fields.PhoneNumber(required=True)


class SerializationSchema(ApiSchema):
    verify_key = fields.Str(default=None)
    expires_in = fields.Int(default=180)


async def OAuthSmsPost(request):
    data = DeserializationSchema().deserialize(await request.json())
    session = OAuthSession(key=data['number'],
                           app=request.app)
    if await session.is_exists():
        result, expires_in = await session.get_data()
        result['expires_in'] = expires_in
        return SerializationSchema().serialize(result)

    verify_key = generate_uuid1()
    code = generate_code()
    session.data = {
        "verify_key": verify_key,
        "code": code
    }
    request.app.logger.info(f'{data["number"]} - {code}')
    await session.save()
    return SerializationSchema().serialize(session.data)
