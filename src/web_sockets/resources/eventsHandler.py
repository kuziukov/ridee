from aiohttp.web import (
    WebSocketResponse
)
from web_sockets.services.decorator import (
    websocket_required
)


@websocket_required
async def eventsHandler(request):
    app = request.app

    ws = WebSocketResponse()
    await ws.prepare(request)

    return ws
