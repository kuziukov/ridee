import aiohttp


class WSocketEchoHandler(object):
    def __init__(self, socket):
        self._ws = socket

    async def listen(self):
        async for msg in self._ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await self._ws.close()
                else:
                    try:
                        await self._ws.send_str(msg.data + '/answer')
                    except Exception:
                        await self._ws.close()
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      self._ws.exception())

        return self._ws
