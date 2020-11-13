from api.resources.users.schemas import UserSchema
from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


class DeserializationSchema(ApiSchema):

    chat_id = fields.ObjectID(required=True)
    message = fields.Str(required=True)
    random_id = fields.Str(required=True)


class DeserializationMessageSchema(ApiSchema):

    start_message_id = fields.ObjectID(required=False)
    count = fields.Int(missing=20)
    offset = fields.Int(missing=0)


class MessageSchema(ApiSchema):

    _id = fields.ObjectID(default=None)
    user = fields.Nested(UserSchema, default=None)
    chat = fields.Nested('MinimalChatSchema', default=None)
    message = fields.Str(default=None)
    created_at = fields.Timestamp()


class MinimalMessageSchema(ApiSchema):

    _id = fields.ObjectID(default=None)
    user = fields.Nested(UserSchema, default=None)
    message = fields.Str(default=None)
    created_at = fields.Timestamp()


class ListMessageSchema(ApiSchema):

    messages = fields.List(fields.Nested(MinimalMessageSchema))
    count = fields.Int()