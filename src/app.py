from aiohttp import web
import asyncio
from config import Config
from cores.rest_core.resource import response
from extentions import (
    init_cors,
    init_redis,
    init_mongo,
    init_timber,
)
from api import init_routes_app_v1
from web_sockets import (
    init_websocket_routes
)


async def create_app(config=Config):
    app = web.Application()
    app.config = config
    app.middlewares.append(response)
    init_cors(app)
    await init_redis(app)
    await init_mongo(app)
    init_routes_app_v1(app)
    init_timber(app)
    app['sockets'] = {}
    app['tasks'] = {}
    init_websocket_routes(app)
    return app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app(Config))
    web.run_app(app, port=5000)
