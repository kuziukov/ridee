import asyncio


class EventEchoHandler(object):
    def __init__(self, store, socket):
        self._store = store
        self._ws = socket

    async def broadcast(self, topic):
        try:

            channel, *_ = await self._store.subscribe(topic)
            while await channel.wait_message():
                try:
                    message = await channel.get_json()
                    for i in self._ws:
                        await i.send_json(
                            {
                                'type': 'Type',
                                'result': message
                            }
                        )
                except Exception:
                    pass

        except asyncio.CancelledError:
            await self._store.unsubscribe(topic)
            for i in self._ws:
                await i.close()
