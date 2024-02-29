import time
import logging

from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware


class LogResponseTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000

        logging.info(
            f"Request path: {request.url.path}, Response time: {process_time:.2f} ms"
        )

        return response
