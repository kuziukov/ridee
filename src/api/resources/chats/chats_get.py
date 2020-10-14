import pymongo
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
    response = {'chats': []}
    try:
        chats = Chats.find({'members.': ObjectId(request.user['_id'])})
        async for chat in chats:
            last_message = Messages.find({
                'chat': chat._id
            }).sort([('created_at', pymongo.DESCENDING)])
            last_message = await last_message.to_list(1)
            response['chats'].append({
                '_id': chat._id,
                'name': chat.name,
                'created_at': chat.created_at,
                'last_message': last_message[0] if last_message else None
            })
    except Exception as e:
        print(e)
        raise ChatsException()
    return SerializationChatsSchema().serialize(response)



