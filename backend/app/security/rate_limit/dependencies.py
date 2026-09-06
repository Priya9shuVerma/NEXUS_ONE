"""
NEXUS ONE - Rate Limit Dependencies
"""

from fastapi import HTTPException, Request

from app.security.rate_limit.limiter import (
    api_rate_limiter,
    auth_rate_limiter,
    ai_rate_limiter,
)


def get_client_key(request: Request) -> str:

    if request.client:
        return request.client.host

    return "unknown"


async def check_api_rate_limit(request: Request):

    key = get_client_key(request)

    if not api_rate_limiter.is_allowed(key):

        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
        )


async def check_auth_rate_limit(request: Request):

    key = get_client_key(request)

    if not auth_rate_limiter.is_allowed(key):

        raise HTTPException(
            status_code=429,
            detail="Too many authentication attempts. Please try again later.",
        )


async def check_ai_rate_limit(request: Request):

    key = get_client_key(request)

    if not ai_rate_limiter.is_allowed(key):

        raise HTTPException(
            status_code=429,
            detail="AI request limit exceeded. Please try again later.",
        )
