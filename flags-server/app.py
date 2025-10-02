from flask import Flask

from config.config import Config
from config.logger_config import setup_logger
from config.mongo_config import init_mongo
from src.blueprints.routes import register_routes
from src.startup.init_flags import add_default_flags
from src.startup.init_modes import add_default_modes

logger = setup_logger()


def create_app() -> None:
    app = Flask(__name__)
    app.config.from_object(Config)

    init_mongo(app)
    logger.info("MongoDB initialized successfully.")

    register_routes(app)
    logger.info("Routes initialized successfully.")

    add_default_flags()
    logger.info("Default flags initialized successfully.")

    add_default_modes()
    logger.info("Default modes initialized successfully.")

    return app


if __name__ == "__main__":
    app = create_app()

    logger.info("Starting Flask application.")
    app.run(
        host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG_MODE"]
    )
