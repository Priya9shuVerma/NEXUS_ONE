"""
NEXUS ONE - Security Request Monitor

Detects basic suspicious HTTP request patterns.
This module does not block requests by itself.
"""

import re
from typing import Optional


SUSPICIOUS_PATTERNS = [
    r"<script",
    r"javascript:",
    r"union\s+select",
    r"\bor\s+1\s*=\s*1",
    r"\bdrop\s+table\b",
    r"\binsert\s+into\b",
    r"\bdelete\s+from\b",
    r"\bupdate\s+\w+\s+set\b",
    r"\.\./",
    r"%2e%2e",
    r"%3cscript",
]


def detect_suspicious_input(value: Optional[str]) -> bool:
    """
    Return True when a suspicious input pattern is detected.
    """

    if not value:
        return False

    normalized = value.lower()

    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, normalized, re.IGNORECASE):
            return True

    return False


def inspect_request_values(
    path: str,
    query_string: str = "",
    user_agent: str = "",
) -> bool:
    """
    Inspect common request fields.

    Returns True when suspicious activity is detected.
    """

    values = [
        path,
        query_string,
        user_agent,
    ]

    return any(
        detect_suspicious_input(value)
        for value in values
    )
