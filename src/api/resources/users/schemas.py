from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


class SerializationSchema(ApiSchema):

    _id = fields.ObjectID(default=None)
    phone = fields.PhoneNumber(default=None)
