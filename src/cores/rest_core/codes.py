def is_informational(code):
    return 100 <= code <= 199


def is_success(code):
    return 200 <= code <= 299


def is_redirect(code):
    return 300 <= code <= 399


def is_client_error(code):
    return 400 <= code <= 499


def is_server_error(code):
    return 500 <= code <= 599


def get_status(code):
    if is_success(code):
        return 'success'
    elif is_client_error(code):
        return 'client_error'
    elif is_server_error(code):
        return 'server_error'
    elif is_redirect(code):
        return 'redirect'
    elif is_informational(code):
        return 'informational'


OK = 200
CREATED = 201
ACCEPTED = 202
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
NOT_FOUND = 404
NOT_ALLOWED = 410
INTERNAL_SERVER_ERROR = 500