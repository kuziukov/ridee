from api.service.decorator import login_required
from api.resources.chats.schemas import FullChatSchema
from api.service.modules import ChatMethods


@login_required(skip_info=True)
async def ChatGet(request):
    chat = await ChatMethods.get_chat_by_id('5f81f2b73d93fc35b83bd07a')
    return FullChatSchema().serialize(chat)



