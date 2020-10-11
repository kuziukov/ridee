from api.service.decorator import login_required
from api.resources.chats.schemas import (
    FullChatSchema,
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
    chat_id = request.match_info.get('chat_id', None)
    try:
        chat = await ChatMethods.get_chat_by_id(chat_id, user['_id'])
    except Exception as e:
        print(e)
        raise ChatException()
    return FullChatSchema().serialize(chat)



