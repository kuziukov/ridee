from bson import ObjectId
from api.resources.chats.schemas import ChatSchema
from api.service.decorator import login_required
from cores.rest_core import (
    APIException,
    codes,
)
from models import (
    Chats,
    Messages
)


class ChatException(APIException):

    @property
    def message(self):
        return 'Invalid chat id.'

    code = codes.BAD_REQUEST


@login_required()
async def ChatGet(request):
    user = request.user
    chat_id = request.match_info.get('chat_id', None)
    if not chat_id:
        raise ChatException()

    chat = await Chats.find_one({'_id': ObjectId(chat_id), 'members.': ObjectId(user['_id'])})
    chat.last_message = await Messages.last_message(chat._id)
    return ChatSchema().serialize({
        '_id': chat._id,
        'name': chat.name,
        'user': await chat.get_user(),
        'members': await chat.list_members(),
        'created_at': chat.created_at,
        'last_message': chat.last_message
    })



