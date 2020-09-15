from . import codes


class APIException(Exception):
    code = codes.INTERNAL_SERVER_ERROR
    message = 'Unknown error occurred'


class DataError(APIException):

    def __init__(self, message):
        self.message = self.validate_message(message)

    @staticmethod
    def validate_message(message):

        def _validate_message(data):
            for key in data:
                if isinstance(data[key], dict):
                    _validate_message(data[key])
                elif not isinstance(data[key], list):
                    raise Exception('Error message should be wrapped to list')

        _validate_message(message)

        return message

    code = codes.BAD_REQUEST

