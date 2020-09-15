import re
from datetime import timezone, datetime
from marshmallow import fields, ValidationError


class ErrorMessages(dict):

    def __getitem__(self, *args, **kwargs):
        value = super().__getitem__(*args, **kwargs)
        if callable(value):
            return value()
        return value


class BaseField:

    default_error_messages = {
        'required': 'Missing required field'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages = ErrorMessages(self.error_messages)


class Dict(BaseField, fields.Dict):
    pass


class Nested(BaseField, fields.Nested):
    pass


class Function(BaseField, fields.Function):
    pass


class List(BaseField, fields.List):
    pass


class Int(BaseField, fields.Int):
    pass


class Bool(BaseField, fields.Bool):
    pass


class Str(BaseField, fields.Str):
    pass


class Timestamp(BaseField, fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return value
        return value.replace(tzinfo=timezone.utc).timestamp()

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return value
        try:
            return datetime.utcfromtimestamp(float(value))
        except TypeError:
            raise ValidationError('Invalid timestamp')


class Email(BaseField, fields.Str):

    def _serialize(self, value, attr, obj, **kwargs):
        value = super()._serialize(value, attr, obj, **kwargs)
        if value is None:
            return value
        name, domen = value.split('@')

        length = len(name)
        fill = 4
        if length > fill + 2:
            fill = length - 2

        name = name[:2] + '*' * fill + name[length - 2:]
        return f'{name}@{domen}'

    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        if bool(re.match('[^@]+@[^@]+\.[^@]+', value)):
            return value
        raise ValidationError('Invalid email address')


class Password(BaseField, fields.Str):

    def _serialize(self, value, attr, obj, **kwargs):
        value = super()._serialize(value, attr, obj, **kwargs)
        if value is None:
            return value
        return '******'

    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        if bool(re.match('((?=.*\d)(?=.*([a-z]|[A-Z])).{8})', value)):
            return value
        raise ValidationError('Password must contain as many as 8 characters including letter and numeric '
                                      'characters')

