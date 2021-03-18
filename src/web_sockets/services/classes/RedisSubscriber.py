from web_sockets.services.abstracts import (
    Subscriber
)
from .NewMessageResponse import NewMessageResponse
from .WSResponse import WSResponse


class RedisSubscriber(Subscriber):

    def __init__(self, ws):
        self._ws = ws

    """
        Publish message to WebSocket client in format.
    """
    async def update(self, message: dict) -> None:

        wsResponse = WSResponse()
        cmd = message.get('cmd', None)
        args = message.get('args', {})

        if cmd == 'NEW_MESSAGE':
            wsResponse.event_response = NewMessageResponse()

        response = await wsResponse.make_response(args)
        await self._ws.send_json(response)
