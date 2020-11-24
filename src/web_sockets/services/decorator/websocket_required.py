import aiohttp
from api.service import WSSession


def websocket_required(func):
    async def wrapped(request):
        token = request.match_info.get('code', None)
        if not isinstance(token, str) and not token:
            request.app.logger.info(f'{token}: invalid')
            raise aiohttp.web.HTTPUnauthorized()

        session = WSSession(request.app, token)
        if not await session.is_exists():
            request.app.logger.info(f'{token}: session do not exists')
            raise aiohttp.web.HTTPUnauthorized()

        data, expires_in = await session.get_data()
        topic = data['user_id']
        await session.destroy()

        request.topic = topic
        return await func(request)
    return wrapped