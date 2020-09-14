from aiohttp import web
import asyncio
from config import (
    DEBUG
)
from extentions import (
    init_cors
)


async def create_app(loop):
    app = web.Application(debug=DEBUG)
    init_cors(app)
    return app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app(loop))
    web.run_app(app, port=5000)
