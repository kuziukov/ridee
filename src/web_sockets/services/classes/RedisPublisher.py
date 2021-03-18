import asyncio
from web_sockets.services.abstracts import (
    AbstractPublisher,
    Subscriber
)


class RedisPublisher(AbstractPublisher):

    _subscribers = []
    _task = None
    _store = None

    def __init__(self, store, topic):
        self._store = store
        self._topic = topic

    """
        Subscribes user for topic and if task does not exist then 
        creates task for broadcasting
    """
    def subscribe(self, subscriber: Subscriber) -> None:
        if not self._task:
            self._task = asyncio.create_task(self.broadcast())
        self._subscribers.append(subscriber)

    """
        Unsubscribes user from topic and if there are no subscribers then
        cancel task
    """
    def unsibscribe(self, subscriber: Subscriber) -> None:
        self._subscribers.remove(subscriber)
        if len(self._subscribers) == 0:
            if self._task:
                if not self._task.cancelled():
                    self._task.cancel()
            self._task = None

    """
        Notify all subscribers about the message
    """
    async def notifySubscribers(self, message) -> None:
        for subscriber in self._subscribers:
            await subscriber.update(message)

    """
        Subscribes for redis topic and wait the message
        If the message received then call notification method
    """
    async def broadcast(self):
        try:
            channel, *_ = await self._store.subscribe(self._topic)
            while await channel.wait_message():
                message = await channel.get_json()
                await self.notifySubscribers(message)
        except asyncio.CancelledError:
            await self._closeSession()

    """
        Service method to delete task and unsubscribe all subscribers
    """
    async def _closeSession(self):

        await self._store.unsubscribe(self._topic)
        if self._task:
            self._task.cancel()


