from api.resources.users.schemas import UserSchema
from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


class ChatSchema(ApiSchema):

    _id = fields.ObjectID()
    name = fields.Str()
    user_id = fields.ObjectID()
    members = fields.List(fields.Nested(UserSchema))
    created_at = fields.Timestamp()


class SerializationChatsSchema(ApiSchema):

    chats = fields.List(fields.Nested(ChatSchema))
