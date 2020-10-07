import aioredis, config


async def init_redis(app):
    session = await aioredis.create_redis_pool(app.config.SESSION_STORE_URI)
    tmp = await aioredis.create_redis_pool(app.config.TMP_STORE_URI)
    events = await aioredis.create_redis_pool(app.config.EVENTS_STORE_URI)

    async def close_redis(app):
        session.close()
        await session.wait_closed()

    app.on_cleanup.append(close_redis)
    app.session = session
    app.tmp = tmp
    app.events = events

