import json


class WSSession(object):

    def __init__(self, app, key):
        self._session_store = app.wsocket_tmp
        self.data = None
        self._key = key

    async def get_data(self):
        if self.data is None:
            data = await self._session_store.get(self.key)
            expires_in = await self._session_store.ttl(self.key)
            if data is not None:
                self.data = json.loads(data)
        return self.data, expires_in

    async def save(self, expires_in=None):
        if expires_in is None:
            ttl = self._session_store.ttl(self.key)
            if ttl != -1:
                expires_in = ttl
        result = await self._session_store.set(self.key, json.dumps(self.data), expire=expires_in)
        return result

    async def is_exists(self):
        return await self._session_store.exists(self.key)

    async def destroy(self):
        return await self._session_store.delete(self.key)

    @property
    def key(self):
        return self._key.decode('utf-8') if isinstance(self._key, bytes) else self._key

