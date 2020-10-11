from api.service.decorator import login_required
from api.resources.chats.schemas import SerializationChatsSchema
from api.service.modules import ChatMethods


@login_required(skip_info=True)
async def ChatsGet(request):
    chats = await ChatMethods.get_all_chats_by_id(request.user['_id'])
    return SerializationChatsSchema().serialize(chats)



