from bson import ObjectId
from api.resources.messages.schemas import (
    ListMessageSchema,
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

    if not await Chats.is_user_in_chat(ObjectId(chat_id), user._id):
        raise NoAccessException()

    query_kwargs = {'chat': ObjectId(chat_id)}
    if 'start_message_id' in data:
        try:
            start_message = await Messages.find_one({'_id': ObjectId(data['start_message_id']), 'chat': ObjectId(chat_id)})
        except Exception as e:
            raise NoAccessException()
        if start_message:
            query_kwargs['created_at'] = {'$lte': start_message.created_at}

    try:
        messages = await Messages.range_messages(query_kwargs, data['count'], data['offset'])
    except Exception as e:
        raise ParametersException()

    return ListMessageSchema().serialize({
        'messages': messages,
        'count': len(messages)
    })
