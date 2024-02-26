from flask import Blueprint
from flask_cors import cross_origin

from controllers import users_controller


users_route = Blueprint("users_route", __name__)


@users_route.route('/top/general', methods=['GET'])
@cross_origin()
def top_general() -> tuple:
    return users_controller.top_general()


@users_route.route('/addormodify', methods=['POST', 'PUT'])
@cross_origin()
def add_or_modify() -> tuple:
    return users_controller.add_or_modify()