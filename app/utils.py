from fastapi.exceptions import HTTPException


class NotFoundError(HTTPException):
    """Custom exception for not found errors."""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class ExternalServiceError(HTTPException):
    """Custom exception for external service errors."""

    def __init__(self, detail: str = "Service unavailable"):
        super().__init__(status_code=503, detail=detail)
