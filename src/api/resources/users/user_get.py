from api.resources.users.schemas import SerializationSchema
from api.service.decorator.login_required import login_required


@login_required
async def UserGet(request):
    return SerializationSchema().serialize(request.user)