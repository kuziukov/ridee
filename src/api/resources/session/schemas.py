from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


class SessionsSchema(ApiSchema):

    items = fields.List(fields.Str(), default=None)
    totals = fields.Int(default=None)


class SessionSchema(ApiSchema):

    _id = fields.Str(default=None)


class DeserializationRefreshSchema(ApiSchema):

    refresh_token = fields.Str(required=True)
