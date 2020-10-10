from api.service.decorator import login_required
from models.chats import Chats
from api.resources.chats.schemas import SerializationChatsSchema


@login_required(skip_info=True)
async def ChatsGet(request):
    chats = await Chats.get_all_chats_by_id(request.user['_id'])
    return SerializationChatsSchema().serialize(chats)



