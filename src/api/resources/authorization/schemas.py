from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


class DeserializationNumberSchema(ApiSchema):

    number = fields.PhoneNumber(required=True)


class SerializationNumberSchema(ApiSchema):

    verify_key = fields.Str(default=None)
    expires_in = fields.Int(default=180)


class DeserializationNumberCompleteSchema(ApiSchema):

    number = fields.PhoneNumber(required=True)
    verify_key = fields.Str(required=True)
    sms_code = fields.Str(required=True)


class SerializationNumberCompleteSchema(ApiSchema):

    access_token = fields.Str(default=None)
    refresh_token = fields.Str(default=None)
    expires_in = fields.Timestamp(default=None)
