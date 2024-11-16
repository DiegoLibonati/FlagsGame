from typing import Any

from flask import Blueprint

from src.controllers import flags_controller


flags_route = Blueprint("flags_route", __name__)


@flags_route.route('/', methods = ['GET'])
def flags() -> dict[str, Any]:
    return flags_controller.flags()


@flags_route.route('/newflag', methods=['POST'])
def add_flag() -> dict[str, Any]:
    return flags_controller.add_flag()


@flags_route.route('/random/<quantity>', methods=["GET"])
def get_random_flags(quantity: str) -> dict[str, Any]:
    return flags_controller.get_random_flags(quantity)


@flags_route.route('/delete/<id>', methods=["DELETE"])
def delete_flag(id: str) -> dict[str, Any]:
    return flags_controller.delete_flag(id)