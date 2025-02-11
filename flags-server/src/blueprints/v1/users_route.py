from flask import Blueprint
from flask import Response

from src.controllers import users_controller


users_route = Blueprint("users_route", __name__)


@users_route.route('/top/general', methods=['GET'])
def top_general() -> Response:
    return users_controller.top_general()


@users_route.route('/addormodify', methods=['POST', 'PUT'])
def add_or_modify() -> Response:
    return users_controller.add_or_modify()


@users_route.route('/delete/<id>', methods=["DELETE"])
def delete_user(id: str) -> Response:
    return users_controller.delete_user(id)