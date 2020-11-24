from bson import ObjectId

from api.resources.messages.messages_get import NoAccessException
from api.resources.messages.schemas import (
    MessageSchema
)
from api.service import EventPublisher
from api.service.decorators import login_required
from cores.marshmallow_core import ApiSchema, fields
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


class DeserializationSchema(ApiSchema):

    chat_id = fields.ObjectID(required=True)
    message = fields.Str(required=True)
    random_id = fields.Str(required=True)


@login_required()
async def MessagePost(request):
    user = request.user
    data = DeserializationSchema().deserialize(await request.json())

    if not await Chats.is_user_in_chat(data['chat_id'], user._id):
        raise NoAccessException()

    message = Messages()
    message.user = user
    message.chat = ObjectId(data['chat_id'])
    message.message = str(data['message']).strip()
    message.random_id = data['random_id']
    try:
        await message.commit()
    except Exception as e:
        request.app.logger.error(e)
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
            request.app.logger.error(e)
            pass

    return MessageSchema().serialize(response)
