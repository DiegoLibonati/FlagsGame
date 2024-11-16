from typing import Any

from flask import Blueprint

from src.controllers import modes_controller


modes_route = Blueprint("modes_route", __name__)


@modes_route.route('/', methods=['GET'])
def get_modes() -> dict[str, Any]:
    return modes_controller.get_modes()


@modes_route.route('/findmode/<name>', methods=['GET'])
def find_mode(name: str) -> dict[str, Any]:
    return modes_controller.find_mode(name)


@modes_route.route('/newmode', methods=['POST'])
def add_mode() -> dict[str, Any]:
    return modes_controller.add_mode()


@modes_route.route('/mode/top/<mode>', methods=['GET'])
def top_mode(mode: str) -> dict[str, Any]:
    return modes_controller.top_mode(mode)


@modes_route.route('/delete/<id>', methods=["DELETE"])
def delete_mode(id: str) -> dict[str, Any]:
    return modes_controller.delete_mode(id)