from api.resources.session.schemas import SessionsSchema
from api.service.decorators import login_required


@login_required()
async def SessionsDelete(request):
    user = request.user
    session = request.app.session

    keys = await session.keys(f"{user['_id']}:*")
    await session.delete(*keys)
    return SessionsSchema().serialize({
        'items': [key.split(b":")[1] for key in keys],
        'totals': len(keys)
    })
