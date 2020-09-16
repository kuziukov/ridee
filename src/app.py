from aiohttp import web
import asyncio
from config import (
    DEBUG
)
from cores.rest_core.resource import format_errors
from extentions import (
    init_cors,
    init_redis,
)
from api import init_routes_app_v1


async def create_app(loop):
    app = web.Application(debug=DEBUG)
    app.middlewares.append(format_errors)
    init_cors(app)
    await init_redis(app, loop)
    init_routes_app_v1(app)
    return app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app(loop))
    web.run_app(app, port=5000)
