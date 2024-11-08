from typing import Any

from flask import Blueprint

from controllers import users_controller


users_route = Blueprint("users_route", __name__)


@users_route.route('/top/general', methods=['GET'])
def top_general() -> dict[str, Any]:
    return users_controller.top_general()


@users_route.route('/addormodify', methods=['POST', 'PUT'])
def add_or_modify() -> dict[str, Any]:
    return users_controller.add_or_modify()