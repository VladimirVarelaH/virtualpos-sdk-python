"""Custom exceptions for VirtualPOS SDK."""


class VirtualPOSAPIError(Exception):
    """Raised when VirtualPOS returns a non-successful API response."""


class VirtualPOSHTTPError(VirtualPOSAPIError):
    """Raised for HTTP layer errors while calling VirtualPOS."""

    def __init__(self, message: str, status_code: int, payload=None):
        self.status_code = status_code
        self.payload = payload
        super().__init__(message)

