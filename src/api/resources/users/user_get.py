from api.resources.users.schemas import SerializationSchema
from api.service import EventPublisher
from api.service.decorator import login_required


@login_required(skip_info=True)
async def UserGet(request):
    await EventPublisher(request.app).publish(request.user['_id'], SerializationSchema().serialize(request.user))

    return SerializationSchema().serialize(request.user)
