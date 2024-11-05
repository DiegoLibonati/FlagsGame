from typing import Any

from flask import Blueprint

from controllers import flags_controller


flags_route = Blueprint("flags_route", __name__)


@flags_route.route('/', methods = ['GET'])
def flags() -> dict[str, Any]:
    return flags_controller.flags()


@flags_route.route('/newflag', methods=['POST'])
def add_flag() -> dict[str, Any]:
    return flags_controller.add_flag()


@flags_route.route('/<mode>', methods=["GET"])
def get_random_flags(mode: str) -> dict[str, Any]:
    return flags_controller.get_random_flags(mode)