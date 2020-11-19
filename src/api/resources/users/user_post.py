from cores.rest_core import (
    APIException,
    codes
)
from api.service.decorators import login_required
from cores.marshmallow_core import (
    ApiSchema,
    fields
)
from api.resources.users.schemas import UserSchema


class ProfileException(APIException):

    @property
    def message(self):
        return 'Username or surname is wrong. Please check the data.'

    code = codes.BAD_REQUEST


class DeserializationSchema(ApiSchema):
    name = fields.Str()
    surname = fields.Str()


@login_required(skip_info=True)
async def UserPost(request):
    user = request.user
    data = DeserializationSchema().deserialize(await request.json())

    if 'name' in data:
        user.name = data['name']
    if 'surname' in data:
        user.surname = data['surname']

    try:
        await user.commit()
    except Exception as e:
        request.app.logger.error(e)
    return UserSchema().serialize(user)
