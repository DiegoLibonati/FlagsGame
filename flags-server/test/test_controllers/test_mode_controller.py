from typing import Any

from bson import ObjectId
from flask import Flask
from flask.testing import FlaskClient
from pymongo.database import Database

from src.constants.codes import (
    CODE_NOT_FOUND_MODE,
    CODE_SUCCESS_ADD_MODE,
    CODE_SUCCESS_DELETE_MODE,
    CODE_SUCCESS_GET_ALL_MODES,
    CODE_SUCCESS_GET_MODE,
    CODE_SUCCESS_GET_TOP_MODE,
)


class TestAliveEndpoint:
    def test_alive_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/modes/alive")

        assert response.status_code == 200

    def test_alive_returns_correct_structure(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/modes/alive")
        data = response.get_json()

        assert "message" in data
        assert "version_bp" in data
        assert "author" in data
        assert "name_bp" in data

    def test_alive_returns_correct_values(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/modes/alive")
        data = response.get_json()

        assert data["message"] == "I am Alive!"
        assert data["name_bp"] == "Modes"

    def test_alive_returns_json_content_type(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/modes/alive")

        assert response.content_type == "application/json"


class TestGetModesEndpoint:
    def test_get_modes_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/modes/")

        assert response.status_code == 200

    def test_get_modes_returns_correct_structure(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/modes/")
        data = response.get_json()

        assert "code" in data
        assert "message" in data
        assert "data" in data

    def test_get_modes_returns_correct_code(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/modes/")
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_GET_ALL_MODES

    def test_get_modes_returns_empty_list_when_no_modes(
        self, app: Flask, client: FlaskClient, mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})

        response = client.get("/api/v1/modes/")
        data = response.get_json()

        assert data["data"] == []

    def test_get_modes_returns_all_modes(
        self, client: FlaskClient, inserted_modes: list[dict[str, Any]]
    ) -> None:
        response = client.get("/api/v1/modes/")
        data = response.get_json()

        assert len(data["data"]) == len(inserted_modes)


class TestFindModeEndpoint:
    def test_find_mode_returns_200(
        self, client: FlaskClient, inserted_mode: dict[str, Any]
    ) -> None:
        response = client.get(f"/api/v1/modes/{inserted_mode['_id']}")

        assert response.status_code == 200

    def test_find_mode_returns_correct_structure(
        self, client: FlaskClient, inserted_mode: dict[str, Any]
    ) -> None:
        response = client.get(f"/api/v1/modes/{inserted_mode['_id']}")
        data = response.get_json()

        assert "code" in data
        assert "message" in data
        assert "data" in data

    def test_find_mode_returns_correct_code(
        self, client: FlaskClient, inserted_mode: dict[str, Any]
    ) -> None:
        response = client.get(f"/api/v1/modes/{inserted_mode['_id']}")
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_GET_MODE

    def test_find_mode_returns_correct_data(
        self, client: FlaskClient, inserted_mode: dict[str, Any]
    ) -> None:
        response = client.get(f"/api/v1/modes/{inserted_mode['_id']}")
        data = response.get_json()

        assert data["data"]["name"] == inserted_mode["name"]
        assert data["data"]["description"] == inserted_mode["description"]

    def test_find_mode_not_found_returns_404(
        self, app: Flask, client: FlaskClient, mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})
        fake_id = str(ObjectId())

        response = client.get(f"/api/v1/modes/{fake_id}")

        assert response.status_code == 404

    def test_find_mode_not_found_returns_correct_code(
        self, app: Flask, client: FlaskClient, mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})
        fake_id = str(ObjectId())

        response = client.get(f"/api/v1/modes/{fake_id}")
        data = response.get_json()

        assert data["code"] == CODE_NOT_FOUND_MODE


class TestTopModeEndpoint:
    def test_top_mode_returns_200(
        self, client: FlaskClient, inserted_mode: dict[str, Any]
    ) -> None:
        response = client.get(f"/api/v1/modes/{inserted_mode['_id']}/top")

        assert response.status_code == 200

    def test_top_mode_returns_correct_structure(
        self, client: FlaskClient, inserted_mode: dict[str, Any]
    ) -> None:
        response = client.get(f"/api/v1/modes/{inserted_mode['_id']}/top")
        data = response.get_json()

        assert "code" in data
        assert "message" in data
        assert "data" in data

    def test_top_mode_returns_correct_code(
        self, client: FlaskClient, inserted_mode: dict[str, Any]
    ) -> None:
        response = client.get(f"/api/v1/modes/{inserted_mode['_id']}/top")
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_GET_TOP_MODE

    def test_top_mode_returns_list(
        self, client: FlaskClient, inserted_mode: dict[str, Any]
    ) -> None:
        response = client.get(f"/api/v1/modes/{inserted_mode['_id']}/top")
        data = response.get_json()

        assert isinstance(data["data"], list)

    def test_top_mode_not_found_returns_404(
        self, app: Flask, client: FlaskClient, mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})
        fake_id = str(ObjectId())

        response = client.get(f"/api/v1/modes/{fake_id}/top")

        assert response.status_code == 404


class TestAddModeEndpoint:
    def test_add_mode_returns_201(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        sample_mode: dict[str, Any],
    ) -> None:
        mongo_db.modes.delete_many({})

        response = client.post("/api/v1/modes/", json=sample_mode)

        assert response.status_code == 201

    def test_add_mode_returns_correct_structure(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        sample_mode: dict[str, Any],
    ) -> None:
        mongo_db.modes.delete_many({})

        response = client.post("/api/v1/modes/", json=sample_mode)
        data = response.get_json()

        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert "_id" in data["data"]

    def test_add_mode_returns_correct_code(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        sample_mode: dict[str, Any],
    ) -> None:
        mongo_db.modes.delete_many({})

        response = client.post("/api/v1/modes/", json=sample_mode)
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_ADD_MODE

    def test_add_mode_creates_mode_in_database(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        sample_mode: dict[str, Any],
    ) -> None:
        mongo_db.modes.delete_many({})
        initial_count = mongo_db.modes.count_documents({})

        client.post("/api/v1/modes/", json=sample_mode)

        final_count = mongo_db.modes.count_documents({})
        assert final_count == initial_count + 1

    def test_add_mode_returns_created_mode_data(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        sample_mode: dict[str, Any],
    ) -> None:
        mongo_db.modes.delete_many({})

        response = client.post("/api/v1/modes/", json=sample_mode)
        data = response.get_json()

        assert data["data"]["name"] == sample_mode["name"]
        assert data["data"]["description"] == sample_mode["description"]
        assert data["data"]["multiplier"] == sample_mode["multiplier"]
        assert data["data"]["timeleft"] == sample_mode["timeleft"]

    def test_add_mode_with_invalid_data_returns_400(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/modes/", json={"name": "Only Name"})

        assert response.status_code == 400

    def test_add_mode_with_empty_body_returns_400(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/modes/", json={})

        assert response.status_code == 400

    def test_add_mode_duplicate_returns_409(
        self, client: FlaskClient, inserted_mode: dict[str, Any]
    ) -> None:
        duplicate_mode = {
            "name": inserted_mode["name"],
            "description": "Other description",
            "multiplier": 50,
            "timeleft": 45,
        }

        response = client.post("/api/v1/modes/", json=duplicate_mode)

        assert response.status_code == 409


class TestDeleteModeEndpoint:
    def test_delete_mode_returns_200(
        self, client: FlaskClient, inserted_mode: dict[str, Any]
    ) -> None:
        response = client.delete(f"/api/v1/modes/{inserted_mode['_id']}")

        assert response.status_code == 200

    def test_delete_mode_returns_correct_structure(
        self, client: FlaskClient, inserted_mode: dict[str, Any]
    ) -> None:
        response = client.delete(f"/api/v1/modes/{inserted_mode['_id']}")
        data = response.get_json()

        assert "code" in data
        assert "message" in data

    def test_delete_mode_returns_correct_code(
        self, client: FlaskClient, inserted_mode: dict[str, Any]
    ) -> None:
        response = client.delete(f"/api/v1/modes/{inserted_mode['_id']}")
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_DELETE_MODE

    def test_delete_mode_removes_from_database(
        self, client: FlaskClient, inserted_mode: dict[str, Any], mongo_db: Database
    ) -> None:
        initial_count = mongo_db.modes.count_documents({})

        client.delete(f"/api/v1/modes/{inserted_mode['_id']}")

        final_count = mongo_db.modes.count_documents({})
        assert final_count == initial_count - 1

    def test_delete_nonexistent_mode_returns_404(
        self, app: Flask, client: FlaskClient, mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})
        fake_id = str(ObjectId())

        response = client.delete(f"/api/v1/modes/{fake_id}")

        assert response.status_code == 404

    def test_delete_nonexistent_mode_returns_correct_code(
        self, app: Flask, client: FlaskClient, mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})
        fake_id = str(ObjectId())

        response = client.delete(f"/api/v1/modes/{fake_id}")
        data = response.get_json()

        assert data["code"] == CODE_NOT_FOUND_MODE
