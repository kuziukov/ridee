from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


class ChatSchema(ApiSchema):

    _id = fields.ObjectID(default=None)
    name = fields.Str()
    created_at = fields.Timestamp()


class SerializationChatsSchema(ApiSchema):

    chats = fields.List(fields.Nested(ChatSchema))

