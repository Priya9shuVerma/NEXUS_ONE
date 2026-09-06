"""
NEXUS ONE - Security Middleware
"""

import time
import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.security.config import (
    SECURITY_HEADERS_ENABLED,
    REQUEST_MONITORING_ENABLED,
)
from app.security.monitoring.request_monitor import inspect_request_values

logger = logging.getLogger("nexus.security")


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Central security middleware.

    Responsibilities:
    - Request monitoring
    - Suspicious input detection
    - Security headers
    - Request timing
    """

    async def dispatch(self, request: Request, call_next):

        start_time = time.perf_counter()

        client_ip = (
            request.client.host
            if request.client
            else "unknown"
        )

        user_agent = request.headers.get(
            "user-agent",
            ""
        )

        query_string = request.url.query

        suspicious = False

        if REQUEST_MONITORING_ENABLED:
            suspicious = inspect_request_values(
                path=request.url.path,
                query_string=query_string,
                user_agent=user_agent,
            )

        if suspicious:
            logger.warning(
                "Suspicious request detected "
                "method=%s path=%s ip=%s",
                request.method,
                request.url.path,
                client_ip,
            )

        response = await call_next(request)

        if SECURITY_HEADERS_ENABLED:

            response.headers["X-Content-Type-Options"] = "nosniff"

            response.headers["X-Frame-Options"] = "DENY"

            response.headers[
                "Referrer-Policy"
            ] = "strict-origin-when-cross-origin"

            response.headers[
                "Permissions-Policy"
            ] = (
                "camera=(), "
                "microphone=(), "
                "geolocation=()"
            )

            response.headers[
                "Cross-Origin-Opener-Policy"
            ] = "same-origin"

            response.headers[
                "Cross-Origin-Resource-Policy"
            ] = "same-origin"

            response.headers[
                "X-XSS-Protection"
            ] = "0"

        duration = time.perf_counter() - start_time

        logger.info(
            "HTTP request "
            "method=%s path=%s status=%s ip=%s duration=%.4fs",
            request.method,
            request.url.path,
            response.status_code,
            client_ip,
            duration,
        )

        return response
