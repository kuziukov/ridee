from api.service.decorator import login_required
from api.resources.chats.schemas import (
    FullChatSchema,
    DeserializationSchema,
)
from api.service.modules import ChatMethods
from cores.rest_core import (
    APIException,
    codes,
)


class ChatException(APIException):

    @property
    def message(self):
        return 'The chat does not exist.'

    code = codes.BAD_REQUEST


@login_required(skip_info=True)
async def ChatGet(request):
    user = request.user
    data = DeserializationSchema().deserialize(request.rel_url.query)
    try:
        chat = await ChatMethods.get_chat_by_id(data['chat_id'], user['_id'])
    except Exception as e:
        raise ChatException()
    return FullChatSchema().serialize(chat)



