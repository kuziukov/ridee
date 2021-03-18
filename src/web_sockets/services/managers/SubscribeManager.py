from web_sockets.services.classes import RedisPublisher


class SubscribeManager:

    _subscribeManagers = {}

    def __init__(self, store):
        self._store = store

    def __del__(self):
        for manager in self._subscribeManagers:
            del manager

    def get(self, topic):
        if topic not in self._subscribeManagers:
            self._subscribeManagers[topic] = RedisPublisher(self._store, topic)

        return self._subscribeManagers[topic]




