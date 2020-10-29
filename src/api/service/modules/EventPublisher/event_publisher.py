import json
from api.resources.messages.schemas import MessageSchema
from .json_encoder import JSONEncoder


class EventMethods:
    @staticmethod
    def message(data):
        response = MessageSchema().serialize(data)
        return response


class EventPublisher(object):
    def __init__(self, app=None):
        self._store = app.events
        self._methods = None

    async def publish(self, topic: str,
                      sys_type: str,
                      data):
        response = {}
        self._methods = getattr(EventMethods, sys_type, None)
        if callable(self._methods):
            response = self._methods(data)
        response['sys_type'] = sys_type
        await self._store.publish(str(topic), json.dumps(response, cls=JSONEncoder))

    @staticmethod
    def parse(data):
        sys_type = data.pop('sys_type', None)
        _methods = getattr(EventMethods, sys_type)
        return sys_type, data




## await EventPublisher(request.app).publish(request.user['_id'], SerializationSchema().serialize(request.user))