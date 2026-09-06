"""
NEXUS ONE - Security Rate Limiting

Thread-safe in-memory sliding-window rate limiter.

Designed for:
- Authentication protection
- API abuse protection
- AI endpoint protection
- Brute-force mitigation
"""

import time
from collections import defaultdict
from functools import wraps
from threading import Lock
from typing import Callable, Optional

from fastapi import HTTPException, Request


class RateLimiter:
    """
    Thread-safe sliding-window rate limiter.

    Each key maintains a list of request timestamps.
    """

    def __init__(
        self,
        max_requests: int = 60,
        window_seconds: int = 60,
    ):
        if max_requests <= 0:
            raise ValueError("max_requests must be greater than zero")

        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than zero")

        self.max_requests = max_requests
        self.window_seconds = window_seconds

        self._requests = defaultdict(list)
        self._lock = Lock()

    def _cleanup(self, timestamps: list[float], now: float) -> None:
        cutoff = now - self.window_seconds

        timestamps[:] = [
            timestamp
            for timestamp in timestamps
            if timestamp > cutoff
        ]

    def is_allowed(self, key: str) -> bool:
        """
        Record a request if the rate limit has not been exceeded.

        Returns:
            True  -> request allowed
            False -> request blocked
        """

        now = time.time()

        with self._lock:
            timestamps = self._requests[key]

            self._cleanup(timestamps, now)

            if len(timestamps) >= self.max_requests:
                return False

            timestamps.append(now)

            return True

    def remaining(self, key: str) -> int:
        """
        Return the number of requests remaining in the current window.
        """

        now = time.time()

        with self._lock:
            timestamps = self._requests[key]

            self._cleanup(timestamps, now)

            remaining = self.max_requests - len(timestamps)

            return max(0, remaining)

    def retry_after(self, key: str) -> int:
        """
        Return an approximate number of seconds before another request
        should be attempted.
        """

        now = time.time()

        with self._lock:
            timestamps = self._requests[key]

            self._cleanup(timestamps, now)

            if not timestamps:
                return 0

            oldest = min(timestamps)

            retry_after = (
                oldest + self.window_seconds - now
            )

            return max(1, int(retry_after))

    def reset(self, key: str) -> None:
        """
        Reset rate-limit state for a specific key.
        """

        with self._lock:
            self._requests.pop(key, None)

    def clear(self) -> None:
        """
        Clear all rate-limit state.
        """

        with self._lock:
            self._requests.clear()


def get_client_key(request: Request) -> str:
    """
    Build a rate-limit key.

    Currently uses the direct client IP supplied by the ASGI server.

    We intentionally do not blindly trust X-Forwarded-For because that
    header can be spoofed unless a trusted reverse proxy is configured.
    """

    if request.client and request.client.host:
        return request.client.host

    return "unknown"


def create_rate_limit_dependency(
    limiter: RateLimiter,
    include_headers: bool = True,
):
    """
    Create a reusable FastAPI dependency around a RateLimiter.
    """

    async def dependency(request: Request):
        client_key = get_client_key(request)

        allowed = limiter.is_allowed(client_key)

        if not allowed:
            retry_after = limiter.retry_after(client_key)

            if include_headers:
                response = HTTPException(
                    status_code=429,
                    detail="Too many requests. Please try again later.",
                    headers={
                        "Retry-After": str(retry_after),
                        "X-RateLimit-Limit": str(limiter.max_requests),
                        "X-RateLimit-Remaining": "0",
                    },
                )

                raise response

            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later.",
            )

        return True

    return dependency


def rate_limit(
    max_requests: int = 60,
    window: int = 60,
):
    """
    FastAPI dependency factory.

    Existing endpoint compatibility is preserved:

        dependencies=[
            Depends(
                rate_limit(
                    max_requests=3,
                    window=60
                )
            )
        ]
    """

    limiter = RateLimiter(
        max_requests=max_requests,
        window_seconds=window,
    )

    return create_rate_limit_dependency(limiter)


# ============================================================
# GLOBAL APPLICATION LIMITERS
# ============================================================

api_rate_limiter = RateLimiter(
    max_requests=60,
    window_seconds=60,
)


# Authentication endpoints receive stricter protection.
auth_rate_limiter = RateLimiter(
    max_requests=10,
    window_seconds=60,
)


# AI endpoints receive a separate quota.
ai_rate_limiter = RateLimiter(
    max_requests=30,
    window_seconds=60,
)


# ============================================================
# PRE-BUILT DEPENDENCIES
# ============================================================

api_rate_limit = create_rate_limit_dependency(
    api_rate_limiter
)


auth_rate_limit = create_rate_limit_dependency(
    auth_rate_limiter
)


ai_rate_limit = create_rate_limit_dependency(
    ai_rate_limiter
)
