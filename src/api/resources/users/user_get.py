from api.resources.users.schemas import SerializationSchema
from api.service.decorator import token_required


@token_required
async def UserGet(request):
    return SerializationSchema().serialize(request.user)