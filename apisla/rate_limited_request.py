import time
import datetime

#import trio
from muffin import Application, Request, ResponseJSON

app = Application()

origin_clock_start = datetime.datetime.now().timestamp() - time.perf_counter()

def pretty_time(seconds : float) -> str:
	present = time.localtime(origin_clock_start + seconds)
	return str(datetime.datetime(present.tm_year, present.tm_mon, present.tm_mday, present.tm_hour, present.tm_min, present.tm_sec))

@app.route("/")
async def timed_api(request: Request): # Callable?
	received = time.perf_counter() # trio.current_time()
	scheduled = received + 5

	print(f"Request received @ {pretty_time(received)} scheduled to reply @ {pretty_time(scheduled_response)}.")
	#trio.sleep_until(scheduled_response)
	time.sleep(5)
	handled = time.perf_counter() # trio.current_time()
	response = { 	'received': received,
					'scheduled': scheduled,
					'handled': handled,
					'delta': handled-scheduled 
				}

	return ResponseJSON(response)	
