from bson import ObjectId
from api.resources.messages.schemas import (
    DeserializationSchema,
    MessageSchema
)
from api.service import EventPublisher
from api.service.decorator import login_required
from cores.rest_core import (
    APIException,
    codes
)
from models import (
    Messages,
    Chats
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
    message.random_id = data['random_id']
    try:
        await message.commit()
    except Exception as e:
        raise MessageException()

    response = {
        '_id': message._id,
        'user': await message.user.fetch(),
        'chat': await message.chat.fetch(),
        'message': message.message,
        'created_at': message.created_at
    }

    subscribers = await Chats.find_one({'_id': ObjectId(data['chat_id'])})
    for member in subscribers.members:
        try:
            await EventPublisher(request.app).publish(topic=member.pk, sys_type='message', data=response)
        except Exception as e:
            print(e)
            pass

    return MessageSchema().serialize(response)


