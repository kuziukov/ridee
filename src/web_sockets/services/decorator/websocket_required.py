import aiohttp
from web_sockets.services import WSSession


def websocket_required(func):
    async def wrapped(request):
        token = request.match_info.get('code', None)
        if not isinstance(token, str) and not token:
            raise aiohttp.web.HTTPUnauthorized()

        print("connected")


        return await func(request)
    return wrapped