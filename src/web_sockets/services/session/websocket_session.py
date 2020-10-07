import json


class WSSession(object):

    def __init__(self, app, key):
        self._session_store = app.wsocket_tmp
        self.data = None
        self._key = key

    async def is_exists(self):
        return await self._session_store.exists(self.key)

    async def destroy(self):
        return await self._session_store.delete(self.key)

    @property
    def key(self):
        return self._key.decode('utf-8') if isinstance(self._key, bytes) else self._key

