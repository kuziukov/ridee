import json
from api.tests.conftest import test_client


async def test_user_post(test_client):
    resp = await test_client.get('/v1.0/user')
    assert resp.status == 200
    response = json.loads(await resp.text())
    assert 'code' in response
    assert response['code'] == 401
    assert 'status' in response
    assert response['status'] == 'client_error'
    assert 'result' in response
    assert response['result'] is not None


async def test_user_post_failed(test_client):
    headers = {'content-type': 'image/gif',
               'Token': '123456'}
    payload = {

    }
    resp = await test_client.post('/v1.0/user', data=payload, headers=headers)
    assert resp.status == 200
    response = json.loads(await resp.text())