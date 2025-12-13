from app.utils import ExternalServiceError, NotFoundError


def test_not_found_error_with_default_message():
    error = NotFoundError()
    assert error.status_code == 404
    assert error.detail == "Resource not found"


def test_not_found_error_with_custom_message():
    error = NotFoundError(detail="Custom not found message")
    assert error.status_code == 404
    assert error.detail == "Custom not found message"


def test_external_service_error_with_default_message():
    error = ExternalServiceError()
    assert error.status_code == 503
    assert error.detail == "Service unavailable"


def test_external_service_error_with_custom_message():
    error = ExternalServiceError(detail="Custom service error message")
    assert error.status_code == 503
    assert error.detail == "Custom service error message"
