import trio

from muffin import TestClient as Client

from ..sla_tracker import app
# from apisla.rate_limited_request import timed_api

async def test_sla_app():
    client = Client(app)

    data = {
        "nonce": "96d1b807-abec-4c08-8ca5-0c47a10d28ac",
        "ip": "127.0.0.1",
        "received": trio.current_time(),
        "sla": "default",
        "req_api": "www.google.com"
        }
    response = await client.post('/rated-req/', data=data, timeout=6)
    assert response.status_code == 200
    assert await response.text() == 'OK'

async def test_sla_app_429():
    client = Client(app)

    status_codes = []
    
    
    async def call_client(array, client, i):
        data = {
        "nonce": f"96d1b807-abec-4c08-8ca5-0c47a10d28a{i}",
        "ip":  "128.0.0.1",
        "received": trio.current_time(),
        "sla": "default",
        "req_api": "www.google.com"
        }
        result = await client.post('/rated-req', data=data, timeout=6)
        text = await result.json()
        status_codes.append((result.status_code, i, text))

    client = Client(app)
    array = []
    async with trio.open_nursery() as nursery:
        for i in range(8):
            await trio.sleep(0.5)
            nursery.start_soon(call_client, array, client, i)


    assert len(status_codes) == 8
    print(status_codes)
    assert status_codes[4][0] == 429