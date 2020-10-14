from bson import ObjectId

from api.service.decorator import login_required
from api.resources.chats.schemas import SerializationChatsSchema
from cores.rest_core import (
    APIException,
    codes,
)
from models import Chats


class ChatsException(APIException):

    @property
    def message(self):
        return 'You do not have any chats available.'

    code = codes.BAD_REQUEST


@login_required(skip_info=True)
async def ChatsGet(request):
    try:
        chats = Chats.find({'members.': ObjectId(request.user['_id'])})
        result = {
            'chats': [document async for document in chats]
        }
    except Exception as e:
        raise ChatsException()
    return SerializationChatsSchema().serialize(result)



