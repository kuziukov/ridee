import pymongo
from bson import ObjectId
from api.resources.chats.schemas import ChatSchema
from api.service.decorator import login_required
from cores.rest_core import (
    APIException,
    codes,
)
from models import Chats, Messages


class ChatException(APIException):

    @property
    def message(self):
        return 'The chat does not exist.'

    code = codes.BAD_REQUEST


@login_required(skip_info=True)
async def ChatGet(request):
    user = request.user
    chat_id = request.match_info.get('chat_id', None)
    chat = await Chats.find_one({'_id': ObjectId(chat_id)})

    last_message = Messages.find({
        'chat': chat._id,
        'user': ObjectId(user['_id'])
    })
    last_message.sort([('created_at', pymongo.DESCENDING)])
    last_message = await last_message.to_list(1)
    return ChatSchema().serialize({
        '_id': chat._id,
        'name': chat.name,
        'user': await chat.user.fetch(),
        'members': [await user.fetch() for user in chat.members],
        'created_at': chat.created_at,
        'last_message': last_message[0] if last_message else None
    })



