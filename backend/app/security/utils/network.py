"""
NEXUS ONE - Security Network Utilities
"""

from fastapi import Request


def get_client_ip(request: Request) -> str:
    """
    Safely obtain the client IP.

    X-Forwarded-For is only trusted when the application is deployed
    behind a trusted reverse proxy.
    """

    forwarded_for = request.headers.get("X-Forwarded-For")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    if request.client:
        return request.client.host

    return "unknown"
