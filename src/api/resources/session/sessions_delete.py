from api.resources.session.schemas import SessionsSchema
from api.service.decorator import login_required


@login_required()
async def SessionsDelete(request):
    user = request.user
    session = request.app.session

    keys = await session.keys(f"{user['_id']}:*")
    await session.delete(*keys)
    response = {
        'sessions': [key.split(b":")[1] for key in keys],
        'count': len(keys)
    }
    return SessionsSchema().serialize(response)
