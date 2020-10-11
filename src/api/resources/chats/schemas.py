from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


class Memebers(ApiSchema):
    user_id = fields.ObjectID()
    created_at = fields.Timestamp()


class FullChatSchema(ApiSchema):

    _id = fields.ObjectID()
    name = fields.Str()
    members = fields.List(fields.Nested(Memebers))
    created_at = fields.Timestamp()


class ChatSchema(ApiSchema):

    _id = fields.ObjectID()
    name = fields.Str()
    created_at = fields.Timestamp()


class SerializationChatsSchema(ApiSchema):

    chats = fields.List(fields.Nested(ChatSchema))

