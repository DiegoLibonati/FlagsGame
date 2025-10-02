from functools import wraps
from typing import Any, Callable, TypeVar, cast

from flask import Response, jsonify
from pydantic import ValidationError
from pymongo.errors import PyMongoError

from config.logger_config import setup_logger
from src.constants.codes import (
    CODE_ERROR_DATABASE,
    CODE_ERROR_GENERIC,
    CODE_ERROR_PYDANTIC,
)
from src.constants.messages import (
    MESSAGE_ERROR_DATABASE,
    MESSAGE_ERROR_GENERIC,
    MESSAGE_ERROR_PYDANTIC,
)
from src.utils.exceptions import BaseAPIError, ValidationAPIError

logger = setup_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def handle_exceptions(func: F) -> F:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Response:
        try:
            return func(*args, **kwargs)

        except BaseAPIError as e:
            logger.warning(f"APIError: {e}")
            return jsonify(e.to_dict()), e.status_code

        except ValidationError as e:
            logger.warning(f"Pydantic validation error: {e.errors()}")

            err = ValidationAPIError(
                code=CODE_ERROR_PYDANTIC,
                message=MESSAGE_ERROR_PYDANTIC,
                payload={"details": e.errors()},
            )
            return jsonify(err.to_dict()), err.status_code

        except PyMongoError as e:
            logger.error(f"MongoDB error: {e}")

            response = {"code": CODE_ERROR_DATABASE, "message": MESSAGE_ERROR_DATABASE}
            return jsonify(response), 500

        except Exception as e:
            logger.exception("Unhandled exception")

            response = {
                "code": CODE_ERROR_GENERIC,
                "message": MESSAGE_ERROR_GENERIC.format(e=str(e)),
            }
            return jsonify(response), 500

    return cast(F, wrapper)
