from bson import ObjectId
from api.service.decorator import login_required
from api.resources.chats.schemas import ChatsSchema
from cores.marshmallow_core import (
    ApiSchema,
    fields
)
from models import (
    Chats,
    Messages
)


class SerializationSchema(ApiSchema):
    items = fields.List(fields.Nested(ChatsSchema))
    totals = fields.Int()


@login_required()
async def ChatsGet(request):
    response = []
    user = request.user
    chats = Chats.find({'members.': ObjectId(user['_id'])})
    async for chat in chats:
        chat.last_message = await Messages.last_message(chat._id)
        response.append(chat)
    return SerializationSchema().serialize({
        'items': response,
        'totals': len(response)
    })
