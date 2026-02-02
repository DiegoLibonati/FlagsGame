from flask import Flask

from src.utils.exceptions import (
    AuthenticationAPIError,
    BaseAPIError,
    BusinessAPIError,
    ConflictAPIError,
    InternalAPIError,
    NotFoundAPIError,
    ValidationAPIError,
)


class TestBaseAPIError:
    def test_default_values(self) -> None:
        error = BaseAPIError()

        assert error.status_code == 500
        assert error.message is not None
        assert error.code is not None

    def test_custom_values(self) -> None:
        error = BaseAPIError(
            code="CUSTOM_CODE",
            message="Custom message",
            status_code=418,
        )

        assert error.status_code == 418
        assert error.message == "Custom message"
        assert error.code == "CUSTOM_CODE"

    def test_to_dict(self) -> None:
        error = BaseAPIError(code="TEST", message="Test message")
        result = error.to_dict()

        assert result["code"] == "TEST"
        assert result["message"] == "Test message"

    def test_to_dict_with_payload(self) -> None:
        error = BaseAPIError(code="TEST", message="Test", payload={"detail": "value"})
        result = error.to_dict()

        assert "payload" in result
        assert result["payload"]["detail"] == "value"

    def test_flask_response(self, app: Flask) -> None:
        with app.app_context():
            error = BaseAPIError(code="TEST", message="Test", status_code=400)
            response, status_code = error.flask_response()

            assert status_code == 400


class TestSpecificErrors:
    def test_validation_error_status_code(self) -> None:
        error = ValidationAPIError(code="VAL", message="Validation failed")
        assert error.status_code == 400

    def test_authentication_error_status_code(self) -> None:
        error = AuthenticationAPIError(code="AUTH", message="Auth failed")
        assert error.status_code == 401

    def test_not_found_error_status_code(self) -> None:
        error = NotFoundAPIError(code="NF", message="Not found")
        assert error.status_code == 404

    def test_conflict_error_status_code(self) -> None:
        error = ConflictAPIError(code="CONF", message="Conflict")
        assert error.status_code == 409

    def test_business_error_status_code(self) -> None:
        error = BusinessAPIError(code="BUS", message="Business rule")
        assert error.status_code == 422

    def test_internal_error_status_code(self) -> None:
        error = InternalAPIError(code="INT", message="Internal")
        assert error.status_code == 500

    def test_all_errors_inherit_from_base(self) -> None:
        error_classes = [
            ValidationAPIError,
            AuthenticationAPIError,
            NotFoundAPIError,
            ConflictAPIError,
            BusinessAPIError,
            InternalAPIError,
        ]

        for cls in error_classes:
            assert issubclass(cls, BaseAPIError)
