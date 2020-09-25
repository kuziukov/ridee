import json

from api.tests.conftest import test_client


async def test_user_get(test_client):
    resp = await test_client.get('/v1.0/user')
    assert resp.status == 200
    response = json.loads(await resp.text())


async def test_user_get_failed(test_client):
    resp = await test_client.get('/v1.0/user')
    assert resp.status == 200
    response = json.loads(await resp.text())
    assert 'code' in response
    assert response['code'] == 401
    assert 'status' in response
    assert response['status'] == 'client_error'
    assert 'result' in response
    assert response['result'] is not None
