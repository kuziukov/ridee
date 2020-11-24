from api.resources.users.schemas import UserSchema
from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


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
    read = fields.List(fields.Nested(UserSchema), default=[])
    created_at = fields.Timestamp()


class MessagesSchema(ApiSchema):

    items = fields.List(fields.Nested(MinimalMessageSchema))
    totals = fields.Int()