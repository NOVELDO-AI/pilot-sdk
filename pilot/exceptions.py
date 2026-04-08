"""Custom exceptions for the PILOT SDK."""


class PilotError(Exception):
    """Base exception for all PILOT SDK errors."""

    def __init__(self, message: str, status_code: int | None = None, body: dict | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class AuthenticationError(PilotError):
    """Raised when API key or token is invalid or missing (401/403)."""


class NotFoundError(PilotError):
    """Raised when a requested resource does not exist (404)."""


class ValidationError(PilotError):
    """Raised when the server rejects the request payload (422)."""


class RateLimitError(PilotError):
    """Raised when the API rate limit is exceeded (429)."""


class ServerError(PilotError):
    """Raised on 5xx server errors."""
