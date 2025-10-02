from flask import Response, jsonify, request

from src.constants.codes import (
    CODE_ERROR_VALUE_IS_NOT_INTEGER,
    CODE_SUCCESS_ADD_FLAG,
    CODE_SUCCESS_DELETE_FLAG,
    CODE_SUCCESS_GET_ALL_FLAGS,
)
from src.constants.messages import (
    MESSAGE_ERROR_VALUE_IS_NOT_INTEGER,
    MESSAGE_SUCCESS_ADD_FLAG,
    MESSAGE_SUCCESS_DELETE_FLAG,
    MESSAGE_SUCCESS_GET_ALL_FLAGS,
)
from src.models.flag_model import FlagModel
from src.services.flag_service import FlagService
from src.utils.error_handler import handle_exceptions
from src.utils.exceptions import ValidationAPIError
from src.utils.helpers import is_positive_integer


@handle_exceptions
def alive() -> Response:
    response = {
        "message": "I am Alive!",
        "version_bp": "2.0.0",
        "author": "Diego Libonati",
        "name_bp": "Flags",
    }

    return jsonify(response), 200


@handle_exceptions
def flags() -> Response:
    flags = FlagService.get_all_flags()

    response = {
        "code": CODE_SUCCESS_GET_ALL_FLAGS,
        "message": MESSAGE_SUCCESS_GET_ALL_FLAGS,
        "data": flags,
    }

    return jsonify(response), 200


@handle_exceptions
def add_flag() -> Response:
    body = request.json
    flag = FlagModel(**body)

    result = FlagService.add_flag(flag=flag)

    data = {"_id": str(result.inserted_id), **flag.model_dump()}

    response = {
        "code": CODE_SUCCESS_ADD_FLAG,
        "message": MESSAGE_SUCCESS_ADD_FLAG,
        "data": data,
    }

    return jsonify(response), 201


@handle_exceptions
def get_random_flags(quantity: str) -> Response:
    if not is_positive_integer(quantity):
        raise ValidationAPIError(
            code=CODE_ERROR_VALUE_IS_NOT_INTEGER,
            message=MESSAGE_ERROR_VALUE_IS_NOT_INTEGER,
        )

    quantity = int(quantity)

    flags = FlagService.get_random_flags(quantity)

    response = {
        "code": CODE_SUCCESS_GET_ALL_FLAGS,
        "message": MESSAGE_SUCCESS_GET_ALL_FLAGS,
        "data": flags,
    }

    return jsonify(response), 200


@handle_exceptions
def delete_flag(id: str) -> Response:
    FlagService.delete_flag_by_id(id)

    response = {
        "code": CODE_SUCCESS_DELETE_FLAG,
        "message": MESSAGE_SUCCESS_DELETE_FLAG,
    }

    return jsonify(response), 200
