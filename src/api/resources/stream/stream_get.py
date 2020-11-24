from api.resources.stream.schemas import StreamSchema
from api.service import EventSession
from api.service.decorators import login_required


@login_required()
async def StreamGet(request):
    user = request.user
    session = await EventSession(request.app).create_session(user)
    result = {
        'endpoint': 'wss://api.ftraveler.com/',
        'key': session.key,
    }
    return StreamSchema().serialize(result)
