from decimal import Decimal

class RatedReq:

    def __init__(
        self,
        ip: str,
        sla: str,
    ):
        self._ip = ip
        self._sla = sla
        self._req_history = []

    @property
    def ip(self):
        return self._ip
    
    @property
    def sla(self):
        return self._sla

    @property
    def req_history(self):
        return self._req_history


    def allow_request(self):
        # default allows 10 requests per 7.5 seconds
        # changing to 4/3
        if self.sla == "default":

            sorted_list = sorted(self._req_history, key=lambda x: x["received"], reverse=True)
            print(f"length? : {len(sorted_list)}")
            print(f"sorted_list: {sorted_list}")
            if len(sorted_list) > 4:
                print(f"quick maffs: {Decimal(sorted_list[0]['received']) - Decimal(sorted_list[3]['received'])}")
                if Decimal(sorted_list[0]["received"]) - Decimal(sorted_list[3]["received"]) > 3:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return "invalid sla"

    def add_req(self, nonce, received, req_api, completed=None):
        self._req_history.insert(0, {
                "nonce" : nonce,
                "received": received,
                "completed": completed,
                "req_api": req_api
                }
            )
        if len(self._req_history) > 20:
            sorted_list = sorted(self.req_history, key=lambda x: x["received"])
            sorted_list.pop(-1)
            self._req_history = sorted_list
    
    def get_req(self, nonce):
        for req in self._req_history:
            if req["nonce"] == nonce:
                return req

    def get_most_recent_completed(self):
        pass

    def update_req_completed(self, nonce, completed):
        for request in self._req_history:
            if request["nonce"] == nonce:
                request["completed"] = completed

        