from bson import ObjectId
from api.service.decorator import login_required
from api.resources.chats.schemas import SerializationChatsSchema
from cores.rest_core import (
    APIException,
    codes,
)
from models import (
    Chats,
    Messages
)


class ChatsException(APIException):

    @property
    def message(self):
        return 'You do not have any chats available.'

    code = codes.BAD_REQUEST


@login_required(skip_info=True)
async def ChatsGet(request):
    user = request.user
    response = []
    chats = Chats.find({'members.': ObjectId(user['_id'])})
    async for chat in chats:
        chat.last_message = await Messages.last_message(chat._id)
        response.append(chat)
    return SerializationChatsSchema().serialize({
        'chats': response,
        'count': len(response)
    })
