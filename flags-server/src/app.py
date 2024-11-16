import os

from flask import Flask
from flask_pymongo import PyMongo

from src.blueprints.v1.flags_route import flags_route
from src.blueprints.v1.modes_route import modes_route
from src.blueprints.v1.users_route import users_route


app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


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

   
if __name__ == "__main__":
    init()
    app.run(debug=True, host = "0.0.0.0", port = app.config["PORT"])
    