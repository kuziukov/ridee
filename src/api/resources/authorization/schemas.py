from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


class DeserializationSchema(ApiSchema):

    code = fields.Str(required=True)
    number = fields.Str(required=True)

