from flask import Blueprint
from flask_cors import cross_origin

from controllers import flags_controller


flags_route = Blueprint("flags_route", __name__)


@flags_route.route('/', methods = ['GET'])
@cross_origin()
def flags() -> tuple:
    return flags_controller.flags()


@flags_route.route('/newflag', methods=['POST'])
def add_flag() -> tuple:
    return flags_controller.add_flag()


@flags_route.route('/<mode>', methods=["GET"])
@cross_origin()
def get_random_flags(mode: str) -> tuple:
    return flags_controller.get_random_flags(mode)