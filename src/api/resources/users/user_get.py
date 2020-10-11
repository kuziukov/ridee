from api.resources.users.schemas import UserSchema
from api.service.decorator import login_required


@login_required(skip_info=True)
async def UserGet(request):
    return UserSchema().serialize(request.user)
