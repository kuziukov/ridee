from aiohttp import web
import asyncio
from config import Config
from cores.rest_core.resource import response
from extentions import (
    init_cors,
    init_redis,
    init_mongo,
)
from api import init_routes
from web_sockets import (
    init_ws_routes
)
from web_sockets.services.managers import (
    SubscribeManager
)


async def create_app(config=Config):
    app = web.Application()
    app.config = config
    app.middlewares.append(response)
    init_cors(app)

    await init_redis(app)
    await init_mongo(app)

    # init_timber(app)
    app.websocket = SubscribeManager(app.events)
    app['sockets'] = {}
    app['tasks'] = {}

    init_routes(app)
    init_ws_routes(app)
    return app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app(Config))
    web.run_app(app, port=5000)
