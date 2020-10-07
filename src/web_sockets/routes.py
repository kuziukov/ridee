from web_sockets.resources import (
    eventsHandler
)


def init_websocket_routes(app):
    app.router.add_route('GET', '/{code}', eventsHandler)
