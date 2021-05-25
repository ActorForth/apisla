import re
import time
import datetime
import trio

from decimal import Decimal, getcontext
from muffin import Application, Request, ResponseJSON
from slatracker.rated_request import RatedReq

app = Application(debug=True)

# configure more when we have it
SLA_RATE = 0.75 # r/s

request_history = {}


origin_clock_start = datetime.datetime.now().timestamp() - time.perf_counter()


async def update_request_object(ip, nonce, received, req_api, sla="default", completed=None):
    if ip in request_history.keys():
        request = request_history[ip]
        request.add_req(nonce, received, req_api)
        print(request.req_history)
    else:
        request = RatedReq(ip, sla)
        request.add_req(nonce, received, req_api)
        request_history[ip] = request
    return request_history[ip]



async def check_loads(): # pragma: no cover
    # TODO
    return

@app.route("/respond-at/", methods=["POST"])
async def respond_at(request: Request):
    if request.method=='POST':
        data = await request.data()
        ip = data["ip"]
        completed = data["completed"]
        req_api = data["req_api"] # call metrics function eventually
        nonce = ["nonce"]
        print(f"request_history: {request_history}")
        requests_from_ip = request_history[ip]
        this_request = requests_from_ip.get_req(nonce)
        requests_from_ip.update_req_completed(nonce, completed)
        # implement sla timing restrictions here.
        
        # for now responds at current time, we would want it to check 
        # the most recent completed time and base off of that
        return trio.current_time()


@app.route("/rated-req/", methods=["POST"])
async def schedule_response(request: Request):
    '''
    This endpoint takes a POST with the following:
    ip:str
    received time:str of a float
    nonce - uuid4:str

    this should only return a time to schedule
    if too many requests return 429
    if this request is within 1 second of previous request, set warning flag.
    if within 1 second and flag set, return 429
    
    if not, set warning flag to false


    '''
    data = await request.data()
    print(data)
    ip = data["ip"]
    received = data["received"]
    nonce = data["nonce"]
    sla = data["sla"]
    req_api = data["req_api"]
    
    if req_api == "http://rest.bch.actorforth.net/":

        return 200, {"scheduled": trio.current_time()} # scheduled time

    if "http://rest.bch.actorforth.net/public/" in req_api:

        return 200, {"scheduled": trio.current_time()} # scheduled time

    # log the request, returning the request object
    request_obj = await update_request_object(
        ip=ip,
        nonce=nonce,
        received=received,
        req_api=req_api,
        sla=sla        
        )

    if request_obj.allow_request():
        return 200, {"scheduled": trio.current_time()} # scheduled time
    else:
        return 429, {"error": "too many requests, please wait and resubmit"}
