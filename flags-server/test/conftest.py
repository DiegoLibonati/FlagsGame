import os
import subprocess
import time
from typing import Any, Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from pymongo import MongoClient
from pymongo.database import Database

from app import create_app
from config.mongo_config import mongo
from src.services.encrypt_service import EncryptService

TEST_MONGO_HOST = os.getenv("TEST_MONGO_HOST", "localhost")
TEST_MONGO_PORT = int(os.getenv("TEST_MONGO_PORT", "27018"))
TEST_MONGO_USER = os.getenv("TEST_MONGO_USER", "admin")
TEST_MONGO_PASS = os.getenv("TEST_MONGO_PASS", "secret123")
TEST_MONGO_DB = os.getenv("TEST_MONGO_DB", "test_db")
TEST_MONGO_URI = f"mongodb://{TEST_MONGO_USER}:{TEST_MONGO_PASS}@{TEST_MONGO_HOST}:{TEST_MONGO_PORT}/{TEST_MONGO_DB}?authSource=admin"


def is_mongo_ready(uri: str, timeout: int = 30) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=1000)
            client.admin.command("ping")
            client.close()
            return True
        except Exception:
            time.sleep(1)
    return False


def start_docker_compose() -> None:
    compose_file = os.path.join(
        os.path.dirname(__file__), "..", "test.docker-compose.yml"
    )

    if not os.path.exists(compose_file):
        raise FileNotFoundError(
            f"The docker-compose file was not found: {compose_file}"
        )

    subprocess.run(
        ["docker", "compose", "-f", compose_file, "up", "-d", "--wait"],
        check=True,
        capture_output=True,
    )


def stop_docker_compose() -> None:
    compose_file = os.path.join(
        os.path.dirname(__file__), "..", "test.docker-compose.yml"
    )

    subprocess.run(
        ["docker", "compose", "-f", compose_file, "down", "-v"],
        check=False,
        capture_output=True,
    )


def clean_all_collections(db: Database) -> None:
    for collection_name in db.list_collection_names():
        db[collection_name].delete_many({})


@pytest.fixture(scope="session")
def docker_compose_up() -> Generator[None, None, None]:
    skip_docker = os.getenv("SKIP_DOCKER_COMPOSE", "").lower() in ("true", "1", "yes")

    if not skip_docker:
        print("\n🐳 Starting test containers...")
        try:
            start_docker_compose()
        except subprocess.CalledProcessError as e:
            print(f"Error starting docker-compose: {e}")
            raise

    if not is_mongo_ready(TEST_MONGO_URI):
        raise RuntimeError("MongoDB is unavailable after the timeout.")

    print("✅ MongoDB ready for testing.")

    yield

    if not skip_docker:
        print("\n🧹 Stopping test containers...")
        stop_docker_compose()


@pytest.fixture(scope="session")
def mongo_client(
    docker_compose_up: Generator[None, None, None]
) -> Generator[MongoClient, None, None]:
    client = MongoClient(TEST_MONGO_URI)
    yield client
    client.close()


@pytest.fixture(scope="session")
def mongo_db(mongo_client: MongoClient) -> Database:
    return mongo_client[TEST_MONGO_DB]


@pytest.fixture(scope="function")
def clean_db(mongo_db: Database) -> Generator[Database, None, None]:
    clean_all_collections(mongo_db)

    yield mongo_db

    clean_all_collections(mongo_db)


@pytest.fixture(scope="function")
def app(mongo_db: Database) -> Generator[Flask, None, None]:
    os.environ["MONGO_URI"] = TEST_MONGO_URI
    os.environ["MONGO_DB_NAME"] = TEST_MONGO_DB
    os.environ["MONGO_HOST"] = TEST_MONGO_HOST
    os.environ["MONGO_PORT"] = str(TEST_MONGO_PORT)

    clean_all_collections(mongo_db)

    application = create_app("testing")
    application.config["TESTING"] = True

    mongo.client = MongoClient(TEST_MONGO_URI)
    mongo.db = mongo.client[TEST_MONGO_DB]

    with application.app_context():
        yield application

    clean_all_collections(mongo_db)

    if mongo.client:
        mongo.client.close()


@pytest.fixture(scope="function")
def client(app: Flask) -> FlaskClient:
    return app.test_client()


# ============================================================================
# Test data fixtures
# ============================================================================


@pytest.fixture
def sample_flag() -> dict[str, str]:
    return {
        "name": "Argentina",
        "image": "https://example.com/argentina.png",
    }


@pytest.fixture
def sample_flags() -> list[dict[str, str]]:
    return [
        {"name": "Argentina", "image": "https://example.com/argentina.png"},
        {"name": "Brasil", "image": "https://example.com/brasil.png"},
        {"name": "Chile", "image": "https://example.com/chile.png"},
    ]


@pytest.fixture
def inserted_flag(
    app: Flask, mongo_db: Database, sample_flag: dict[str, str]
) -> dict[str, str]:
    mongo_db.flags.delete_many({})
    result = mongo_db.flags.insert_one(sample_flag.copy())
    return {**sample_flag, "_id": str(result.inserted_id)}


@pytest.fixture
def inserted_flags(
    app: Flask, mongo_db: Database, sample_flags: list[dict[str, str]]
) -> list[dict[str, str]]:
    mongo_db.flags.delete_many({})
    inserted = []
    for flag in sample_flags:
        result = mongo_db.flags.insert_one(flag.copy())
        inserted.append({**flag, "_id": str(result.inserted_id)})
    return inserted


@pytest.fixture
def sample_mode() -> dict[str, Any]:
    return {
        "name": "Test Mode",
        "description": "Test mode description",
        "multiplier": 10,
        "timeleft": 90,
    }


@pytest.fixture
def sample_modes() -> list[dict[str, Any]]:
    return [
        {
            "name": "Normal",
            "description": "Normal mode",
            "multiplier": 10,
            "timeleft": 90,
        },
        {"name": "Hard", "description": "Hard mode", "multiplier": 100, "timeleft": 60},
        {
            "name": "Hardcore",
            "description": "Hardcore mode",
            "multiplier": 1000,
            "timeleft": 30,
        },
    ]


@pytest.fixture
def inserted_mode(
    app: Flask, mongo_db: Database, sample_mode: dict[str, Any]
) -> dict[str, Any]:
    mongo_db.modes.delete_many({})
    result = mongo_db.modes.insert_one(sample_mode.copy())
    return {**sample_mode, "_id": str(result.inserted_id)}


@pytest.fixture
def inserted_modes(
    app: Flask, mongo_db: Database, sample_modes: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    mongo_db.modes.delete_many({})
    inserted = []
    for mode in sample_modes:
        result = mongo_db.modes.insert_one(mode.copy())
        inserted.append({**mode, "_id": str(result.inserted_id)})
    return inserted


@pytest.fixture
def sample_user() -> dict[str, Any]:
    return {
        "username": "testuser",
        "password": "testpassword123",
        "scores": {"General": 100, "Normal": 100},
        "total_score": 100,
    }


@pytest.fixture
def sample_users() -> list[dict[str, Any]]:
    return [
        {
            "username": "user1",
            "password": "pass1",
            "scores": {"General": 100, "Normal": 100},
            "total_score": 100,
        },
        {
            "username": "user2",
            "password": "pass2",
            "scores": {"General": 200, "Hard": 200},
            "total_score": 200,
        },
        {
            "username": "user3",
            "password": "pass3",
            "scores": {"General": 150, "Hardcore": 150},
            "total_score": 150,
        },
    ]


@pytest.fixture
def inserted_user(
    app: Flask, mongo_db: Database, sample_user: dict[str, Any]
) -> dict[str, Any]:
    mongo_db.users.delete_many({})
    user_copy = sample_user.copy()
    user_copy["password"] = EncryptService(user_copy["password"]).password_hashed
    result = mongo_db.users.insert_one(user_copy)
    return {
        **sample_user,
        "_id": str(result.inserted_id),
        "hashed_password": user_copy["password"],
    }


@pytest.fixture
def inserted_users(
    app: Flask, mongo_db: Database, sample_users: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    mongo_db.users.delete_many({})

    inserted = []
    for user in sample_users:
        user_copy = user.copy()
        user_copy["password"] = EncryptService(user_copy["password"]).password_hashed
        result = mongo_db.users.insert_one(user_copy)
        inserted.append(
            {
                **user,
                "_id": str(result.inserted_id),
                "hashed_password": user_copy["password"],
            }
        )
    return inserted
