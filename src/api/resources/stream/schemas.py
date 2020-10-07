from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


class SerializationSchema(ApiSchema):

    endpoint = fields.Str(default=None)
    key = fields.Str(default=None)
