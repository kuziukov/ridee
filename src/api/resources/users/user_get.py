from api.resources.users.schemas import PersonalUserSchema
from api.service.decorator import login_required


@login_required()
async def UserGet(request):
    user = request.user
    return PersonalUserSchema().serialize(user)

