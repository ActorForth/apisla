import time
import datetime
import httpx
import json
import os
import trio
import trio.testing
import uuid

from muffin import Application, Request, ResponseJSON

app = Application(debug=True)

origin_clock_start = datetime.datetime.now().timestamp() - time.perf_counter()

SLA_TRACKER_HOST = os.environ.get("SLA_TRACKER_HOST", "127.0.0.1")
SLA_TRACKER_PORT = os.environ.get("SLA_TRACKER_PORT", "2424")

def pretty_time(seconds : float) -> str:
	present = time.localtime(origin_clock_start + seconds)
	return str(datetime.datetime(present.tm_year, present.tm_mon, 
			   present.tm_mday, present.tm_hour, present.tm_min, present.tm_sec))


async def schedule_request(ip, nonce, time, url):
	async with httpx.AsyncClient() as client:
		response = await client.post(
			f"http://{SLA_TRACKER_HOST}:{SLA_TRACKER_PORT}/rated-req/",
			data={
				"ip": ip,
				"received": time,
				"nonce": nonce,
				"req_api": url,
				"sla": "default"
				}
			)
		result = response.json()
		return result

async def get_response_time(ip, apireq, nonce, completed):
	async with httpx.AsyncClient() as client:
		r = await client.post(
			f"http://{SLA_TRACKER_HOST}:{SLA_TRACKER_PORT}/respond-at/",
			data={
				"ip": ip,
				"completed": completed,
				"nonce": nonce,
				"req_api": apireq
				}
			)
		result = r.json()
		return result
	

async def update_metrics():
	# TODO update metrics with response data
	pass

async def call_external_api(url):
	print(f"NOT MOCKED")
	async with httpx.AsyncClient() as client:
		r = await client.get(url)
		result = r.json()
		return r.status_code, result


@app.route("/", methods=["POST"])
async def timed_api(request: Request): # Callable?
	print(f"headers: {request.headers}")
	received = time.perf_counter() # trio.current_time()

	# create nonce
	nonce = uuid.uuid4
	ip="0"
	request_data = await request.data()

	ip = request_data["ip"]
	url = request_data["url"]

	received_time = trio.current_time()

	# get scheduled from sla tracker


	result = await schedule_request(ip, nonce, received, url)
	scheduled = result["scheduled"]

	scheduled = trio.current_time()

	print(f"Request received @ {pretty_time(received_time)} scheduled to reply @ {pretty_time(scheduled)}.")
	await trio.sleep_until(scheduled)

	# call external service
	status, result = await call_external_api(url)
	if not status == 200:
		return 502, "API unreachable at this time"
	 
	completed = trio.current_time()

	# call sla tracker again to get respond time
	respond_at=0
	if request.method == 'POST':
		respond_at = await get_response_time(
			ip=ip,
			apireq=url,
			nonce=nonce,
			completed=completed
		)

	await trio.sleep_until(respond_at)

	# handled = time.perf_counter() # trio.current_time()
	handled = trio.current_time()

	# update metrics
	# call sla-tracker

	result["meta"] = {
				"sla":{
					"received": received_time,
					"scheduled": scheduled,
					"handled": handled,
					"delta": handled-scheduled
				}
			}
	
	return 200, result

