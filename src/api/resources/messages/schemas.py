from api.resources.users.schemas import UserSchema
from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


class DeserializationSchema(ApiSchema):

    user_id = fields.ObjectID(required=True)
    chat_id = fields.ObjectID(required=True)
    message = fields.Str(required=True)
