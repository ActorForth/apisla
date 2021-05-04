sequenceDiagram
    participant C as Client
    participant N as HTTPS Proxy (Nginx)
    participant R as Rate Limited Request
    participant S as Service
    participant SLA as SLA Tracker
    autonumber

    C->>N:Https Request
    N->>R: Req: API=url, Source=IP, SLA=none (default)
    activate R
    Note left of R: New Rate Limited Request is spawned with connection socket.
    Note over R: Unique Nonce is established.
    Note over R: RatedRed: Req, Nonce, Received=time::now
    R->>SLA: RatedReq
    Note over SLA: Records API request w/RatedReq.Nonce
    Note over SLA: Checks load for target service.
    Note over SLA: Determine when req should be submitted.
    SLA-->>R: RequestSchedule: RatedReq.None, RequestAt=timestamp
    Note over R: Rate Limited Request is put on scheduled request queue.
    deactivate R
    R-)R: wait_until RequestSchedule.RequestAt
    activate R
    R->>S: Req
    S-->>R: Response
    Note over R: RatedResp: Response, Completed=time::now
    Note over R: (Assume successful Response)
    R->>SLA: ApiTime: RatedReq, Req.API, Completed=time::now
    Note over SLA: Records API fullfillment w/RatedReq.Nonce.
    Note over SLA: Determine appropriate response time.
    SLA-->>R: ResponseSchedule: RatedReq.Nonce, RespondAt=timestamp
    deactivate R
    Note over R: Rate Limited Request is put on scheduled return queue.
    R-)R: wait_until ResponseSchedule.RespondAt
    activate R
    R-->>C: Response (possibly with SLA meta data)   
    Note right of N: Will the socket handle https for us or need to use Nginx proxy?
    Note over R: RespondedAt=time::now     
    R->>SLA: Response.Status, RatedReq.Nonce, RespondedAt
    Note over SLA: Updates actual performance metrics with Nonce.
    Note over SLA: Re-evaluates proper response times.
    deactivate R
    Note left of R: Rate Limited Request Destructs
    