import time
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time


        logging.info(
            f"""
            Method: {request.method}
            URL: {request.url.path}
            Status: {response.status_code}
            Time: {process_time:.4f}s
            """
        )


        return response