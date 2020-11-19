from api.resources.session.schemas import SessionsSchema
from api.service.decorators import login_required


@login_required()
async def SessionsGet(request):
    user = request.user
    session = request.app.session

    keys = await session.keys(f"{user['_id']}:*")
    return SessionsSchema().serialize({
        'items': [key.split(b":")[1] for key in keys],
        'totals': len(keys)
    })

