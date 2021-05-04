import trio
import apisla.app

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
	client = TestClient(app)
	response = await client.get('/')
	assert response.status_code == 200
	assert await response.text() == 'OK'