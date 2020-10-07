from aiohttp import (
    web
)
from aiohttp.web_exceptions import (
    HTTPException
)
from . import (
    codes,
    APIException
)


@web.middleware
async def response(request, handler):
    try:
        data = await handler(request)
        code = codes.OK
    except HTTPException as e:
        code = e.status
        data = {'error': e.__class__.__name__, 'message': e.text, }
    except APIException as e:
        code = e.code
        data = {'error': e.__class__.__name__, 'message': e.message,}
    except Exception as e:
        print(e)
        code = codes.INTERNAL_SERVER_ERROR
        data = {'error': 'InternalServerError', 'message': 'Internal Server Error.', }
    return web.json_response(
        {
            'code': code,
            'status': codes.get_status(code),
            'result': data
        }
    )