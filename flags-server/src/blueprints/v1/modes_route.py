from flask import Blueprint
from flask import Response

from src.controllers import modes_controller


modes_route = Blueprint("modes_route", __name__)


@modes_route.route('/', methods=['GET'])
def get_modes() -> Response:
    return modes_controller.get_modes()


@modes_route.route('/findmode/<name>', methods=['GET'])
def find_mode(name: str) -> Response:
    return modes_controller.find_mode(name)


@modes_route.route('/newmode', methods=['POST'])
def add_mode() -> Response:
    return modes_controller.add_mode()


@modes_route.route('/mode/top/<mode>', methods=['GET'])
def top_mode(mode: str) -> Response:
    return modes_controller.top_mode(mode)


@modes_route.route('/delete/<id>', methods=["DELETE"])
def delete_mode(id: str) -> Response:
    return modes_controller.delete_mode(id)