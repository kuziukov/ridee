from cores.marshmallow_core import fields
from cores.marshmallow_core.schema import ApiSchema


class UserSchema(ApiSchema):

    _id = fields.ObjectID(default=None)
    name = fields.Str()
    surname = fields.Str()
    region_code = fields.Str(default=None)
    phone = fields.PhoneNumber(default=None, load_only=True)


class CoodrinationSchema(ApiSchema):

    lat = fields.Float(default=0)
    long = fields.Float(default=0)


class PersonalUserSchema(ApiSchema):

    _id = fields.ObjectID(default=None)
    name = fields.Str()
    surname = fields.Str()
    region_code = fields.Str(default=None)
    phone = fields.PhoneNumber(default=None, load_only=True)
    last_coord = fields.Nested(CoodrinationSchema)

