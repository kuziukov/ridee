from api.resources.session.schemas import SessionSchema
from api.service import Session
from api.service.decorator import login_required
from cores.rest_core import APIException, codes


class SessionIDException(APIException):

    @property
    def message(self):
        return 'Wrong Session ID.'

    code = codes.BAD_REQUEST


class SessionExpiredException(APIException):

    @property
    def message(self):
        return 'The session expired.'

    code = codes.BAD_REQUEST


@login_required()
async def SessionDelete(request):
    user = request.user

    session_id = request.match_info.get('session_id', None)
    if not session_id:
        raise SessionIDException()

    session = Session(request.app, f'{user["_id"]}:{session_id}')
    if not await session.is_exists():
        raise SessionExpiredException()

    await session.destroy()
    response = {
        '_id': session.key.split(':')[1]
    }
    return SessionSchema().serialize(response)

