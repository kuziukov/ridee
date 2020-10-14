import pymongo
from bson import ObjectId
from api.resources.messages.schemas import (
    ShortMessageSchema
)
from api.service.decorator import login_required
from cores.rest_core import (
    APIException,
    codes
)
from models import (
    Messages,
    Chats)


class ParametersException(APIException):

    @property
    def message(self):
        return 'Required parameters are wrong.'

    code = codes.BAD_REQUEST


class NoAccessException(APIException):

    @property
    def message(self):
        return 'You have no access to the chat'

    code = codes.BAD_REQUEST


@login_required(skip_info=True)
async def MessagesGet(request):
    user = request.user
    chat_id = request.match_info.get('chat_id', None)
    try:
        count = 200 if int(request.rel_url.query.get('count', 20)) >= 200 else int(request.rel_url.query.get('count', 20))
    except Exception as e:
        raise ParametersException()

    chat = None
    try:
        chat = await Chats.find_one({'_id': ObjectId(chat_id), 'members.': user._id})
    except Exception as e:
        raise NoAccessException()

    if not chat:
        raise NoAccessException()

    messages = Messages.find({
        'chat': chat._id
    }).sort([('created_at', pymongo.DESCENDING)])
    messages = await messages.to_list(count)

    return ShortMessageSchema().serialize({
        'messages': messages
    })
