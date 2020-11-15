from api.resources.stream.schemas import StreamSchema
from api.service import EventSession
from api.service.decorator import login_required


@login_required()
async def StreamGet(request):
    user = request.user
    session = await EventSession(request.app).create_session(user)
    result = {
        'endpoint': 'https://api.ftraveler.com/',
        'key': session.key,
    }
    return StreamSchema().serialize(result)
