import json


class WSSession(object):

    def __init__(self, app):
        self.data = None
        self._session_store = app.session

    async def is_exists(self):
        return await self._session_store.exists(self.key)

    async def destroy(self):
        return await self._session_store.delete(self.key)
