import aiohttp


async def eventsHandler(request):
    app = request.app
    store = request.app.notification_store
    topic = request.match_info.get('code', None)

    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)

    return ws
