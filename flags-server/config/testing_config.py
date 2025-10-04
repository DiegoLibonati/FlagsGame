import os

from config.default_config import DefaultConfig


class TestingConfig(DefaultConfig):
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://admin:secret123@host.docker.internal:27017/flags_test?authSource=admin",
    )

    TESTING = True
    DEBUG = True
    ENV = "testing"
