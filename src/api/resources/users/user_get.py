from api.resources.users.schemas import SerializationSchema
from api.service.decorator import login_required


@login_required(skip_info=True)
async def UserGet(request):
    return SerializationSchema().serialize(request.user)
