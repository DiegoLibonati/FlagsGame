import os

# BLUEPRINTS
BLUEPRINTS = {
    "flags": "/api/v1/flags",
    "modes": "/api/v1/modes",
    "users": "/api/v1/users",
}

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PROJECT_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
COMPOSE_FILE = os.path.join(PROJECT_ROOT, "dev.docker-compose.yml")
