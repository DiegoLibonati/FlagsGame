import os

from flask import Flask
from flask_pymongo import PyMongo

from src.blueprints.v1.flags_route import flags_route
from src.blueprints.v1.modes_route import modes_route
from src.blueprints.v1.users_route import users_route
from src.data_access.flags_repository import FlagRepository
from src.data_access.modes_repository import ModeRepository
from src.utils.constants import DEFAULT_MODES
from src.utils.constants import DEFAULT_FLAGS


app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


def add_default_modes() -> None:
    mode_repository = ModeRepository(db=app.mongo.db)

    modes = mode_repository.get_all_modes()

    if modes: return

    for default_mode in DEFAULT_MODES:
        mode_repository.insert_mode(mode=default_mode)


def add_default_flags() -> None:
    flag_repository = FlagRepository(db=app.mongo.db)

    flags = flag_repository.get_all_flags()

    if flags: return

    for default_flag in DEFAULT_FLAGS:
        flag_repository.insert_flag(flag=default_flag)


def init() -> None:
    # Load Routes
    app.register_blueprint(flags_route, url_prefix="/v1/flags")
    app.register_blueprint(modes_route, url_prefix="/v1/modes")
    app.register_blueprint(users_route, url_prefix="/v1/users")
    
    # Configs
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config['JSON_AS_ASCII'] = False
    app.config["PORT"] = os.getenv("PORT")

    # Mongo
    app.mongo = PyMongo(app)

    # ADD DATA TO DATABASE IF RUNS FOR FIRST
    add_default_modes()
    add_default_flags()

   
if __name__ == "__main__":
    init()
    app.run(debug=True, host = "0.0.0.0", port = app.config["PORT"])
    