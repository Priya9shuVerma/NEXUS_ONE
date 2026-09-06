"""
NEXUS ONE - Security Configuration
"""

# HTTP security headers
SECURITY_HEADERS_ENABLED = True

# Rate limiting
RATE_LIMIT_ENABLED = True

# Request monitoring
REQUEST_MONITORING_ENABLED = True

# Password policy
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128

# JWT
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

# Refresh token lifetime
REFRESH_TOKEN_DAYS = 7

# Security logging
SECURITY_LOGGING_ENABLED = True
