from bson import ObjectId

from api.resources.messages.schemas import DeserializationSchema
from api.service.decorator import login_required
from api.service.modules import MessageMethods
from cores.rest_core import APIException, codes
from models.message import Message


class MessageException(APIException):

    @property
    def message(self):
        return 'The message is not sent. Please check data and try again.'

    code = codes.BAD_REQUEST


@login_required(skip_info=True)
async def MessagePost(request):
    user = request.user
    data = DeserializationSchema().deserialize(await request.json())

    message = Message()
    message.user_id = ObjectId(data['user_id'])
    message.chat_id = ObjectId(data['chat_id'])
    message.message = data['message']
    try:
        pass
        #result = await MessageMethods.message(message)
    except Exception as e:
        print(e)
        raise MessageException()


