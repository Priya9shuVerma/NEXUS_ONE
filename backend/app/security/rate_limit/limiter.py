from fastapi import HTTPException, Request
from time import time
from collections import defaultdict


# Store request timestamps per IP
requests = defaultdict(list)



def rate_limit(
    max_requests: int = 5,
    window: int = 60
):

    async def limiter(request: Request):

        client_ip = request.client.host

        current_time = time()


        # Remove old requests outside window
        requests[client_ip] = [
            timestamp
            for timestamp in requests[client_ip]
            if current_time - timestamp < window
        ]


        # Check limit
        if len(requests[client_ip]) >= max_requests:

            raise HTTPException(
                status_code=429,
                detail={
                    "success": False,
                    "message": "Too many requests. Please try again later."
                }
            )


        # Add current request timestamp
        requests[client_ip].append(current_time)


    return limiter