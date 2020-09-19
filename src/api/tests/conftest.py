import pytest
from app import create_app


@pytest.fixture
async def test_client(aiohttp_client, loop):
    app = await create_app(loop)
    return await aiohttp_client(app)
