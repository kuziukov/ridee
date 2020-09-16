from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


class DeserializationSchema(ApiSchema):

    number = fields.PhoneNumber(required=True)

