from api.resources.authorization.schemas import (
    DeserializationNumberSchema,
    SerializationNumberSchema
)
from api.service.session.authorization import AuthorizationSession
from utils import generate_uuid1, generate_sms_code


async def AuthorizationSmsPost(request):

    data = DeserializationNumberSchema().deserialize(await request.json())
    session = AuthorizationSession(data['number'], app=request.app)
    if await session.is_exists():
        result, expires_in = await session.get_data()
        result["expires_in"] = expires_in
        return SerializationNumberSchema().serialize(result)

    verify_key = generate_uuid1()
    sms_code = generate_sms_code()
    session.data = {
        "verify_key": verify_key,
        "sms_code": sms_code
    }
    print(sms_code)
    await session.save()
    return SerializationNumberSchema().serialize(session.data)

