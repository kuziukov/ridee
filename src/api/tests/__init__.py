from aiohttp.test_utils import AioHTTPTestCase

from app import create_app
from config import TestConfig


class AppTestCase(AioHTTPTestCase):

    async def get_application(self):
        return await create_app(TestConfig)

    async def tearDownAsync(self) -> None:
        await self.app.db.client.drop_database(self.app.db)
