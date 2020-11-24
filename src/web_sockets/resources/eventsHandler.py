import asyncio

from aiohttp.web import (
    WebSocketResponse
)
from web_sockets.services import (
    websocket_required,
    EventEchoHandler,
    WSocketEchoHandler
)


@websocket_required
async def EventsHandler(request):
    app = request.app
    topic = request.topic
    events = app.events

    ws = WebSocketResponse()
    await ws.prepare(request)

    if topic not in app['sockets']:
        app['sockets'][topic] = []
        task = asyncio.create_task(EventEchoHandler(events, app['sockets'][topic]).broadcast(topic))
        app['tasks'][topic] = task
    app['sockets'][topic].append(ws)

    try:
        await asyncio.gather(WSocketEchoHandler(ws).listen())
    finally:
        request.app.logger.info(f'{app["sockets"][topic]}: disconnected')
        app['sockets'][topic].remove(ws)
        if len(app['sockets'][topic]) == 0:
            app['sockets'].pop(topic)
            task = app['tasks'].pop(topic)
            task.cancel()
    return ws
