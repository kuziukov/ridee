import json


class OAuthSession(object):

    def __init__(self, key, app):
        self._key = key
        self.data = None
        self._tmp_store = app.tmp

    async def is_exists(self):
        return await self._tmp_store.exists(self.key)

    async def destroy(self):
        return await self._tmp_store.delete(self.key)

    async def get_data(self):
        if self.data is None:
            data = await self._tmp_store.get(self.key)
            expires_in = await self._tmp_store.ttl(self.key)
            if data is not None:
                self.data = json.loads(data)
        return self.data, expires_in

    async def save(self):
        expires_in = 180
        result = await self._tmp_store.set(self.key, json.dumps(self.data), expire=expires_in)
        return result

    @property
    def key(self):
        return self._key.decode('utf-8') if isinstance(self._key, bytes) else self._key

