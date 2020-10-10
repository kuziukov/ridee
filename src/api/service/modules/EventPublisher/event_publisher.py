import json
from .json_encoder import JSONEncoder


class EventPublisher(object):
    def __init__(self, app):
        self._store = app.events

    async def publish(self, topic: str, data: dict):
        response = {
            'type': None,
            'data': json.dumps(data, cls=JSONEncoder)
        }
        await self._store.publish(str(topic), response)
