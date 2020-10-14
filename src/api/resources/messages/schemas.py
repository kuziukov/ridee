from api.resources.users.schemas import UserSchema
from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


class DeserializationSchema(ApiSchema):

    chat_id = fields.ObjectID(required=True)
    message = fields.Str(required=True)


class MessageSchema(ApiSchema):

    _id = fields.ObjectID(default=None)
    message = fields.Str(default=None)
    created_at = fields.Timestamp()


class ShortMessageSchema(ApiSchema):

    _id = fields.ObjectID(default=None)