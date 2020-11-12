from api.resources.session.schemas import SessionsSchema
from api.service.decorator import login_required


@login_required(skip_info=True)
async def SessionsGet(request):
    user = request.user
    session = request.app.session

    keys = await session.keys(f"{user['_id']}:*")
    response = {
        'sessions': [key.split(b":")[1] for key in keys],
        'count': len(keys)
    }
    return SessionsSchema().serialize(response)

