from marshmallow import (
    Schema as OriginSchema,
    ValidationError
)
from cores.rest_core.exceptions import DataError


class Schema(OriginSchema):

    def get_attribute(self, obj, attr, default):
        value = super().get_attribute(obj, attr, default)
        if value is None:
            return default
        return value


class ApiSchema(Schema):

    def deserialize(self, data, many=None, unknown='unknown'):
        try:
            data = self.load(data, many=many, unknown=unknown)
        except ValidationError as e:
            raise DataError(e.messages)
        return data

    def serialize(self, data, many=None):
        return self.dump(data, many=many)

