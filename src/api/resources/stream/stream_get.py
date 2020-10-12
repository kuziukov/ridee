from api.resources.stream.schemas import StreamSchema
from api.service.decorator import login_required
from web_sockets.services import EventSession


@login_required()
async def StreamGet(request):
    user = request.user
    session = await EventSession(request.app).create_session(user)
    result = {
        'endpoint': 'https://api.wlusm.ru/',
        'key': session.key,
    }
    return StreamSchema().serialize(result)
