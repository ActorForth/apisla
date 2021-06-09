import trio
import pytest

from muffin import TestClient as Client
from unittest import mock
from apisla import app
from apisla import rate_limited_request
from apisla.rate_limited_request import call_external_api, timed_api
from apisla._tests.samples import (
    external_address_details
)

def mocked_external(*args, **kwargs):

    return 200, external_address_details

async def mocked_sla_tracker(*args, **kwargs):

    return 1

# We can just use 'async def test_*' to define async tests.
# This also uses a virtual clock fixture, so time passes quickly and
# predictably.
async def test_sleep_with_autojump_clock(autojump_clock):
    assert trio.current_time() == 0

    for i in range(10):
        print("Sleeping {} seconds".format(i))
        start_time = trio.current_time()
        await trio.sleep(i)
        end_time = trio.current_time()

        assert end_time - start_time == i

async def test_app():
	client = Client(app)
	response = await client.get('/', timeout=6)
	assert response.status_code == 405

@mock.patch("apisla.rate_limited_request.httpx.post")
@mock.patch("apisla.rate_limited_request.httpx.get", side_effect=mocked_external)
async def test_post(mock1, mock2):
    mock2.side_effect = [

    ]
    client = Client(app)
    data = {"ip": 1,
            "url": "https://rest.bch.actorforth.org/v2/address/details/bitcoincash:qzs02v05l7qs5s24srqju498qu55dwuj0cx5ehjm2c"}
    response = await client.post("/", data=data, timeout=6)
    print(f"response: {response}")
    response = await response.json()
    assert response["slpAddress"] == external_address_details["slpAddress"]


async def test_call_external():
    result = await call_external_api("http://rest.bch.actorforth.org/v2/address/details/bitcoincash:qq2p3c6qyjtctr4gwul9pazl5n5pxex9syd8rrupy4")
    print(f"result: {result}")
    assert result.status_code == 200