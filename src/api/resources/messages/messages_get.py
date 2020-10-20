import pymongo
from bson import ObjectId
from api.resources.messages.schemas import (
    ShortMessageSchema,
    DeserializationMessageGetSchema
)
from api.service.decorator import login_required
from cores.rest_core import (
    APIException,
    codes
)
from models import (
    Messages,
    Chats
)


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
    data = DeserializationMessageGetSchema().deserialize(request.rel_url.query)

    try:
        chat = await Chats.find_one({'_id': ObjectId(chat_id), 'members.': user._id})
    except Exception as e:
        raise NoAccessException()
    if not chat:
        raise NoAccessException()

    query_kwargs = {'chat': chat._id}
    if 'start_message_id' in data:
        try:
            start_message = await Messages.find_one({'_id': ObjectId(data['start_message_id']), 'chat': chat._id})
        except Exception as e:
            raise NoAccessException()
        if not start_message:
            raise ParametersException()
        query_kwargs['created_at'] = {'$lte': start_message.created_at}

    try:
        messages = Messages.find(query_kwargs).sort([('created_at', pymongo.DESCENDING)]).skip(data['offset'])
        messages = await messages.to_list(data['count'])
    except Exception as e:
        raise ParametersException()

    return ShortMessageSchema().serialize({
        'messages': messages
    })
