from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta


from local_log import local_logger


class RateLimitingMiddleware(BaseHTTPMiddleware):
    # Rate limiting configurations
    RATE_LIMIT_DURATION = timedelta(minutes=10)
    RATE_LIMIT_REQUESTS = 3
    BLOCK_IPS = ['']

    def __init__(self, app):
        super().__init__(app)
        # Dictionary to store request counts for each IP
        self.request_counts = {}

    async def dispatch(self, request, call_next):
        # Get the client's IP address
        client_ip = request.client.host
        local_logger.info(f"Client IP: {client_ip}")

        if client_ip in self.BLOCK_IPS:
            return JSONResponse(
                status_code=423,
                content={"message": f"{client_ip} is banned"}
            )

        # Check if IP is already present in request_counts
        request_count, last_request = self.request_counts.get(client_ip, (0, datetime.min))

        # Calculate the time elapsed since the last request
        elapsed_time = datetime.now() - last_request

        if elapsed_time > self.RATE_LIMIT_DURATION:
            # If the elapsed time is greater than the rate limit duration, reset the count
            request_count = 1
        else:
            if request_count >= self.RATE_LIMIT_REQUESTS:
                # If the request count exceeds the rate limit, return a JSON response with an error message
                return JSONResponse(
                    status_code=429,
                    content={"message": "Rate limit exceeded. Please try again later."}
                )
            request_count += 1

        # Update the request count and last request timestamp for the IP
        self.request_counts[client_ip] = (request_count, datetime.now())

        # Proceed with the request
        response = await call_next(request)
        return response
