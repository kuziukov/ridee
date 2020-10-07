import json
from .json_encoder import JSONEncoder


class EventPublisher(object):
    def __init__(self, app):
        self._store = app.events

    async def publish(self, topic: str, data: dict):
        await self._store.publish(str(topic), json.dumps(data, cls=JSONEncoder))
