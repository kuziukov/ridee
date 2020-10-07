from web_sockets.resources import (
    EventsHandler
)


def init_websocket_routes(app):
    app.router.add_route('GET', '/{code}', EventsHandler)
