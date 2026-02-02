from bson import ObjectId
from flask import Flask
from flask.testing import FlaskClient
from pymongo.database import Database

from src.constants.codes import (
    CODE_ERROR_VALUE_IS_NOT_INTEGER,
    CODE_SUCCESS_ADD_FLAG,
    CODE_SUCCESS_DELETE_FLAG,
    CODE_SUCCESS_GET_ALL_FLAGS,
)


class TestAliveEndpoint:
    def test_alive_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/flags/alive")

        assert response.status_code == 200

    def test_alive_returns_correct_structure(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/flags/alive")
        data = response.get_json()

        assert "message" in data
        assert "version_bp" in data
        assert "author" in data
        assert "name_bp" in data

    def test_alive_returns_correct_values(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/flags/alive")
        data = response.get_json()

        assert data["message"] == "I am Alive!"
        assert data["version_bp"] == "2.0.0"
        assert data["author"] == "Diego Libonati"
        assert data["name_bp"] == "Flags"

    def test_alive_returns_json_content_type(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/flags/alive")

        assert response.content_type == "application/json"


class TestFlagsEndpoint:
    def test_flags_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/flags/")

        assert response.status_code == 200

    def test_flags_returns_correct_structure(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/flags/")
        data = response.get_json()

        assert "code" in data
        assert "message" in data
        assert "data" in data

    def test_flags_returns_correct_code(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/flags/")
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_GET_ALL_FLAGS

    def test_flags_returns_empty_list_when_no_flags(
        self, app: Flask, client: FlaskClient, mongo_db: Database
    ) -> None:
        mongo_db.flags.delete_many({})

        response = client.get("/api/v1/flags/")
        data = response.get_json()

        assert data["data"] == []

    def test_flags_returns_all_flags(
        self, client: FlaskClient, inserted_flags: list[dict[str, str]]
    ) -> None:
        response = client.get("/api/v1/flags/")
        data = response.get_json()

        assert len(data["data"]) == len(inserted_flags)


class TestAddFlagEndpoint:
    def test_add_flag_returns_201(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        sample_flag: dict[str, str],
    ) -> None:
        mongo_db.flags.delete_many({})

        response = client.post("/api/v1/flags/", json=sample_flag)

        assert response.status_code == 201

    def test_add_flag_returns_correct_structure(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        sample_flag: dict[str, str],
    ) -> None:
        mongo_db.flags.delete_many({})

        response = client.post("/api/v1/flags/", json=sample_flag)
        data = response.get_json()

        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert "_id" in data["data"]

    def test_add_flag_returns_correct_code(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        sample_flag: dict[str, str],
    ) -> None:
        mongo_db.flags.delete_many({})

        response = client.post("/api/v1/flags/", json=sample_flag)
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_ADD_FLAG

    def test_add_flag_creates_flag_in_database(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        sample_flag: dict[str, str],
    ) -> None:
        mongo_db.flags.delete_many({})
        initial_count = mongo_db.flags.count_documents({})

        client.post("/api/v1/flags/", json=sample_flag)

        final_count = mongo_db.flags.count_documents({})
        assert final_count == initial_count + 1

    def test_add_flag_returns_created_flag_data(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        sample_flag: dict[str, str],
    ) -> None:
        mongo_db.flags.delete_many({})

        response = client.post("/api/v1/flags/", json=sample_flag)
        data = response.get_json()

        assert data["data"]["name"] == sample_flag["name"]
        assert data["data"]["image"] == sample_flag["image"]

    def test_add_flag_with_invalid_data_returns_400(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/flags/", json={"name": "Only Name"})

        assert response.status_code == 400

    def test_add_flag_with_empty_body_returns_400(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/flags/", json={})

        assert response.status_code == 400

    def test_add_flag_duplicate_returns_409(
        self, client: FlaskClient, inserted_flag: dict[str, str]
    ) -> None:
        duplicate_flag = {
            "name": inserted_flag["name"],
            "image": "https://example.com/other.png",
        }

        response = client.post("/api/v1/flags/", json=duplicate_flag)

        assert response.status_code == 409


class TestGetRandomFlagsEndpoint:
    def test_get_random_flags_returns_200(
        self, client: FlaskClient, inserted_flags: list[dict[str, str]]
    ) -> None:
        response = client.get("/api/v1/flags/random/2")

        assert response.status_code == 200

    def test_get_random_flags_returns_correct_structure(
        self, client: FlaskClient, inserted_flags: list[dict[str, str]]
    ) -> None:
        response = client.get("/api/v1/flags/random/2")
        data = response.get_json()

        assert "code" in data
        assert "message" in data
        assert "data" in data

    def test_get_random_flags_returns_correct_code(
        self, client: FlaskClient, inserted_flags: list[dict[str, str]]
    ) -> None:
        response = client.get("/api/v1/flags/random/2")
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_GET_ALL_FLAGS

    def test_get_random_flags_returns_requested_quantity(
        self, client: FlaskClient, inserted_flags: list[dict[str, str]]
    ) -> None:
        response = client.get("/api/v1/flags/random/2")
        data = response.get_json()

        assert len(data["data"]) == 2

    def test_get_random_flags_with_invalid_quantity_returns_400(
        self, client: FlaskClient
    ) -> None:
        response = client.get("/api/v1/flags/random/invalid")

        assert response.status_code == 400

    def test_get_random_flags_with_invalid_quantity_returns_correct_code(
        self, client: FlaskClient
    ) -> None:
        response = client.get("/api/v1/flags/random/invalid")
        data = response.get_json()

        assert data["code"] == CODE_ERROR_VALUE_IS_NOT_INTEGER

    def test_get_random_flags_with_negative_returns_400(
        self, client: FlaskClient
    ) -> None:
        response = client.get("/api/v1/flags/random/-5")

        assert response.status_code == 400

    def test_get_random_flags_with_zero_returns_empty(
        self, client: FlaskClient, inserted_flags: list[dict[str, str]]
    ) -> None:
        response = client.get("/api/v1/flags/random/0")

        assert response.status_code == 400


class TestDeleteFlagEndpoint:
    def test_delete_flag_returns_200(
        self, client: FlaskClient, inserted_flag: dict[str, str]
    ) -> None:
        response = client.delete(f"/api/v1/flags/{inserted_flag['_id']}")

        assert response.status_code == 200

    def test_delete_flag_returns_correct_structure(
        self, client: FlaskClient, inserted_flag: dict[str, str]
    ) -> None:
        response = client.delete(f"/api/v1/flags/{inserted_flag['_id']}")
        data = response.get_json()

        assert "code" in data
        assert "message" in data

    def test_delete_flag_returns_correct_code(
        self, client: FlaskClient, inserted_flag: dict[str, str]
    ) -> None:
        response = client.delete(f"/api/v1/flags/{inserted_flag['_id']}")
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_DELETE_FLAG

    def test_delete_flag_removes_from_database(
        self, client: FlaskClient, inserted_flag: dict[str, str], mongo_db: Database
    ) -> None:
        initial_count = mongo_db.flags.count_documents({})

        client.delete(f"/api/v1/flags/{inserted_flag['_id']}")

        final_count = mongo_db.flags.count_documents({})
        assert final_count == initial_count - 1

    def test_delete_nonexistent_flag_returns_404(
        self, app: Flask, client: FlaskClient, mongo_db: Database
    ) -> None:
        mongo_db.flags.delete_many({})
        fake_id = str(ObjectId())

        response = client.delete(f"/api/v1/flags/{fake_id}")

        assert response.status_code == 404
