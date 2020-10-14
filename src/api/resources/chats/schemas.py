from api.resources.messages.schemas import MessageSchema
from api.resources.users.schemas import UserSchema
from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


class ChatSchema(ApiSchema):

    _id = fields.ObjectID()
    name = fields.Str()
    user = fields.Nested(UserSchema, default=None)
    members = fields.List(fields.Nested(UserSchema))
    created_at = fields.Timestamp()
    last_message = fields.Nested(MessageSchema, default=None)


class ChatsSchema(ApiSchema):

    _id = fields.ObjectID()
    name = fields.Str()
    created_at = fields.Timestamp()
    last_message = fields.Nested(MessageSchema, default=None)


class SerializationChatsSchema(ApiSchema):

    chats = fields.List(fields.Nested(ChatsSchema))
