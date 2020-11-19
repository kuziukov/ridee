from api.resources.users.schemas import PrivateUserSchema
from api.service.decorator import login_required


@login_required()
async def UserGet(request):
    user = request.user
    return PrivateUserSchema().serialize(user)

