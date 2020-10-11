from api.service.decorator import login_required
from api.resources.chats.schemas import SerializationChatsSchema
from api.service.modules import ChatMethods
from cores.rest_core import APIException, codes


class ChatsException(APIException):

    @property
    def message(self):
        return 'You do not have any chats available.'

    code = codes.BAD_REQUEST


@login_required(skip_info=True)
async def ChatsGet(request):
    try:
        chats = await ChatMethods.get_all_chats_by_id(request.user['_id'])
    except Exception as e:
        raise ChatsException()
    return SerializationChatsSchema().serialize(chats)



