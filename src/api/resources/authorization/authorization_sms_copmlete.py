from api.resources.authorization.schemas import (
    SerializationNumberCompleteSchema,
    DeserializationNumberCompleteSchema
)
from api.service.session.authorization import AuthorizationSession
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
            return SerializationNumberCompleteSchema().serialize(result)

    raise CommunityException()

