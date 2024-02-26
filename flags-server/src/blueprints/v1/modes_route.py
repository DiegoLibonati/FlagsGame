from flask import Blueprint
from flask_cors import cross_origin

from controllers import modes_controller


modes_route = Blueprint("modes_route", __name__)


@modes_route.route('/findmode/<name>', methods=['GET'])
@cross_origin()
def find_mode(name: str) -> tuple:
    return modes_controller.find_mode(name)


@modes_route.route('/newmode', methods=['POST'])
@cross_origin()
def add_mode() -> tuple:
    return modes_controller.add_mode()


@modes_route.route('/mode/top/<mode>', methods=['GET'])
@cross_origin()
def top_mode(mode: str) -> tuple:
    return modes_controller.top_mode(mode)