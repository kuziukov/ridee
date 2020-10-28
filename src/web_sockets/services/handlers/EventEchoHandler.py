import asyncio

from api.service import EventPublisher


class EventEchoHandler(object):
    def __init__(self, store, socket):
        self._store = store
        self._ws = socket

    async def _closeSession(self, topic):
        await self._store.unsubscribe(topic)
        for i in self._ws:
            await i.close()

    async def broadcast(self, topic):
        try:
            channel, *_ = await self._store.subscribe(topic)
            while await channel.wait_message():
                try:
                    message = await channel.get_json()
                    type, message = EventPublisher.parse(message)
                    for i in self._ws:
                        await i.send_json({
                            'type': type,
                            'result': message
                        })
                except Exception as e:
                    print(e)
                    pass
        except asyncio.CancelledError:
            await self._closeSession(topic)
