from bson import ObjectId
from api.resources.messages.schemas import (
    DeserializationSchema,
    ShortMessageSchema
)
from api.service.decorator import login_required
from cores.rest_core import (
    APIException,
    codes
)
from models import (
    Messages
)


class MessageException(APIException):

    @property
    def message(self):
        return 'The message is not sent. Please check data and try again.'

    code = codes.BAD_REQUEST


@login_required(skip_info=True)
async def MessagePost(request):
    user = request.user
    data = DeserializationSchema().deserialize(await request.json())

    message = Messages()
    message.user = user
    message.chat = ObjectId(data['chat_id'])
    message.message = data['message']
    message.random_id = "12345"

    try:
        await message.commit()
    except Exception as e:
        print(e)
        raise MessageException()
    return ShortMessageSchema().serialize(message)


