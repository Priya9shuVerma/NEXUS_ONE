import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger("nexus_one.security")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Security-safe HTTP request logging middleware.

    Logs:
    - HTTP method
    - request path
    - response status
    - processing time
    - client IP

    Never logs:
    - Authorization headers
    - passwords
    - access tokens
    - refresh tokens
    - cookies
    - request bodies
    """

    SENSITIVE_PATH_PARTS = (
        "/login",
        "/register",
        "/refresh-token",
        "/logout",
        "/change-password",
    )

    def _get_client_ip(self, request: Request) -> str:
        """
        Get the direct client IP.

        X-Forwarded-For is intentionally not trusted here because it can
        be spoofed unless the application is behind a trusted proxy.
        """

        if request.client and request.client.host:
            return request.client.host

        return "unknown"

    def _safe_path(self, request: Request) -> str:
        """
        Return only the URL path.

        Query parameters are deliberately excluded because they can
        contain credentials, tokens, API keys, or other secrets.
        """

        return request.url.path

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        start_time = time.perf_counter()

        client_ip = self._get_client_ip(request)
        path = self._safe_path(request)

        try:
            response = await call_next(request)

            status_code = response.status_code

            return response

        except Exception:
            status_code = 500

            logger.exception(
                "Unhandled request exception | "
                "method=%s path=%s status=%s client=%s",
                request.method,
                path,
                status_code,
                client_ip,
            )

            raise

        finally:
            process_time = time.perf_counter() - start_time

            logger.info(
                "HTTP request | "
                "method=%s path=%s status=%s time=%.4fs client=%s",
                request.method,
                path,
                status_code,
                process_time,
                client_ip,
            )
