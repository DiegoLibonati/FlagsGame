import os

from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo


from blueprints.v1.flags_route import flags_route
from blueprints.v1.modes_route import modes_route
from blueprints.v1.users_route import users_route


app = Flask(__name__)


def on_init() -> None:
    # Load Routes
    app.register_blueprint(flags_route, url_prefix="/v1/flags")
    app.register_blueprint(modes_route, url_prefix="/v1/modes")
    app.register_blueprint(users_route, url_prefix="/v1/users")
    
    # Configs
    app.config["MONGO_URI"] = "mongodb://flags-db/flags"
    app.config['JSON_AS_ASCII'] = False

    # Mongo
    app.mongo = PyMongo(app)

    # Cors
    CORS(app)

    app.run(debug=True, host = "0.0.0.0", port = os.getenv("PORT"))

    return

if __name__ == "__main__":
    on_init()
    