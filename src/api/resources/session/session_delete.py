from api.resources.session.schemas import SessionSchema
from api.service import Session
from api.service.decorator import login_required
from cores.rest_core import APIException, codes


class SessionIdException(APIException):

    @property
    def message(self):
        return 'Session id invalid.'

    code = codes.BAD_REQUEST


class ExpiredException(APIException):

    @property
    def message(self):
        return 'The session expired.'

    code = codes.BAD_REQUEST


@login_required()
async def SessionDelete(request):
    user = request.user
    app = request.app
    session_id = request.match_info.get('session_id', None)
    if not session_id:
        raise SessionIdException()

    session = Session(app=app,
                      key=f'{user["_id"]}:{session_id}')
    if not await session.is_exists():
        raise ExpiredException()

    await session.destroy()
    return SessionSchema().serialize({
        '_id': session.key.split(':')[1]
    })

