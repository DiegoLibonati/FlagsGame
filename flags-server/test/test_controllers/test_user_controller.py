from typing import Any

from bson import ObjectId
from flask import Flask
from flask.testing import FlaskClient
from pymongo.database import Database

from src.constants.codes import (
    CODE_ERROR_AUTHENTICATION,
    CODE_NOT_FOUND_MODE,
    CODE_NOT_FOUND_USER,
    CODE_SUCCESS_ADD_USER,
    CODE_SUCCESS_DELETE_USER,
    CODE_SUCCESS_GET_GLOBAL_TOP_USER,
    CODE_SUCCESS_UPDATE_USER,
)


class TestAliveEndpoint:
    def test_alive_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/users/alive")

        assert response.status_code == 200

    def test_alive_returns_correct_structure(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/users/alive")
        data = response.get_json()

        assert "message" in data
        assert "version_bp" in data
        assert "author" in data
        assert "name_bp" in data

    def test_alive_returns_correct_values(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/users/alive")
        data = response.get_json()

        assert data["message"] == "I am Alive!"
        assert data["name_bp"] == "Users"

    def test_alive_returns_json_content_type(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/users/alive")

        assert response.content_type == "application/json"


class TestTopGeneralEndpoint:
    def test_top_general_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/users/top_global")

        assert response.status_code == 200

    def test_top_general_returns_correct_structure(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/users/top_global")
        data = response.get_json()

        assert "code" in data
        assert "message" in data
        assert "data" in data

    def test_top_general_returns_correct_code(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/users/top_global")
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_GET_GLOBAL_TOP_USER

    def test_top_general_returns_list(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/users/top_global")
        data = response.get_json()

        assert isinstance(data["data"], list)

    def test_top_general_returns_empty_when_no_users(
        self, app: Flask, client: FlaskClient, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})

        response = client.get("/api/v1/users/top_global")
        data = response.get_json()

        assert data["data"] == []

    def test_top_general_returns_users_sorted_by_score(
        self, client: FlaskClient, inserted_users: list[dict[str, Any]]
    ) -> None:
        response = client.get("/api/v1/users/top_global")
        data = response.get_json()

        assert len(data["data"]) == len(inserted_users)
        scores = [user["score"] for user in data["data"]]
        assert scores == sorted(scores, reverse=True)


class TestAddUserEndpoint:
    def test_add_user_returns_201(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        inserted_mode: dict[str, Any],
    ) -> None:
        mongo_db.users.delete_many({})

        user_data = {
            "username": "newuser",
            "password": "newpassword123",
            "mode_id": inserted_mode["_id"],
            "score": 100,
        }

        response = client.post("/api/v1/users/", json=user_data)

        assert response.status_code == 201

    def test_add_user_returns_correct_structure(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        inserted_mode: dict[str, Any],
    ) -> None:
        mongo_db.users.delete_many({})

        user_data = {
            "username": "newuser",
            "password": "newpassword123",
            "mode_id": inserted_mode["_id"],
            "score": 100,
        }

        response = client.post("/api/v1/users/", json=user_data)
        data = response.get_json()

        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert "_id" in data["data"]

    def test_add_user_returns_correct_code(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        inserted_mode: dict[str, Any],
    ) -> None:
        mongo_db.users.delete_many({})

        user_data = {
            "username": "newuser",
            "password": "newpassword123",
            "mode_id": inserted_mode["_id"],
            "score": 100,
        }

        response = client.post("/api/v1/users/", json=user_data)
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_ADD_USER

    def test_add_user_does_not_return_password(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        inserted_mode: dict[str, Any],
    ) -> None:
        mongo_db.users.delete_many({})

        user_data = {
            "username": "newuser",
            "password": "newpassword123",
            "mode_id": inserted_mode["_id"],
            "score": 100,
        }

        response = client.post("/api/v1/users/", json=user_data)
        data = response.get_json()

        assert "password" not in data["data"]

    def test_add_user_creates_user_in_database(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        inserted_mode: dict[str, Any],
    ) -> None:
        mongo_db.users.delete_many({})
        initial_count = mongo_db.users.count_documents({})

        user_data = {
            "username": "newuser",
            "password": "newpassword123",
            "mode_id": inserted_mode["_id"],
            "score": 100,
        }

        client.post("/api/v1/users/", json=user_data)

        final_count = mongo_db.users.count_documents({})
        assert final_count == initial_count + 1

    def test_add_user_with_invalid_mode_returns_404(
        self, app: Flask, client: FlaskClient, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})
        mongo_db.modes.delete_many({})

        user_data = {
            "username": "newuser",
            "password": "newpassword123",
            "mode_id": str(ObjectId()),
            "score": 100,
        }

        response = client.post("/api/v1/users/", json=user_data)

        assert response.status_code == 404

    def test_add_user_with_invalid_mode_returns_correct_code(
        self, app: Flask, client: FlaskClient, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})
        mongo_db.modes.delete_many({})

        user_data = {
            "username": "newuser",
            "password": "newpassword123",
            "mode_id": str(ObjectId()),
            "score": 100,
        }

        response = client.post("/api/v1/users/", json=user_data)
        data = response.get_json()

        assert data["code"] == CODE_NOT_FOUND_MODE

    def test_add_user_duplicate_returns_409(
        self,
        client: FlaskClient,
        inserted_user: dict[str, Any],
        inserted_mode: dict[str, Any],
    ) -> None:
        user_data = {
            "username": inserted_user["username"],
            "password": "newpassword123",
            "mode_id": inserted_mode["_id"],
            "score": 100,
        }

        response = client.post("/api/v1/users/", json=user_data)

        assert response.status_code == 409


class TestModifyUserEndpoint:
    def test_modify_user_returns_200(
        self,
        client: FlaskClient,
        inserted_user: dict[str, Any],
        inserted_mode: dict[str, Any],
    ) -> None:
        user_data = {
            "username": inserted_user["username"],
            "password": "testpassword123",
            "mode_id": inserted_mode["_id"],
            "score": 200,
        }

        response = client.patch("/api/v1/users/", json=user_data)

        assert response.status_code == 200

    def test_modify_user_returns_correct_structure(
        self,
        client: FlaskClient,
        inserted_user: dict[str, Any],
        inserted_mode: dict[str, Any],
    ) -> None:
        user_data = {
            "username": inserted_user["username"],
            "password": "testpassword123",
            "mode_id": inserted_mode["_id"],
            "score": 200,
        }

        response = client.patch("/api/v1/users/", json=user_data)
        data = response.get_json()

        assert "code" in data
        assert "message" in data
        assert "data" in data

    def test_modify_user_returns_correct_code(
        self,
        client: FlaskClient,
        inserted_user: dict[str, Any],
        inserted_mode: dict[str, Any],
    ) -> None:
        user_data = {
            "username": inserted_user["username"],
            "password": "testpassword123",
            "mode_id": inserted_mode["_id"],
            "score": 200,
        }

        response = client.patch("/api/v1/users/", json=user_data)
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_UPDATE_USER

    def test_modify_user_does_not_return_password(
        self,
        client: FlaskClient,
        inserted_user: dict[str, Any],
        inserted_mode: dict[str, Any],
    ) -> None:
        user_data = {
            "username": inserted_user["username"],
            "password": "testpassword123",
            "mode_id": inserted_mode["_id"],
            "score": 200,
        }

        response = client.patch("/api/v1/users/", json=user_data)
        data = response.get_json()

        assert "password" not in data["data"]

    def test_modify_user_with_invalid_mode_returns_404(
        self, client: FlaskClient, inserted_user: dict[str, Any], mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})

        user_data = {
            "username": inserted_user["username"],
            "password": "testpassword123",
            "mode_id": str(ObjectId()),
            "score": 200,
        }

        response = client.patch("/api/v1/users/", json=user_data)

        assert response.status_code == 404

    def test_modify_user_with_invalid_mode_returns_correct_code(
        self, client: FlaskClient, inserted_user: dict[str, Any], mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})

        user_data = {
            "username": inserted_user["username"],
            "password": "testpassword123",
            "mode_id": str(ObjectId()),
            "score": 200,
        }

        response = client.patch("/api/v1/users/", json=user_data)
        data = response.get_json()

        assert data["code"] == CODE_NOT_FOUND_MODE

    def test_modify_user_not_found_returns_404(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        inserted_mode: dict[str, Any],
    ) -> None:
        mongo_db.users.delete_many({})

        user_data = {
            "username": "nonexistentuser",
            "password": "testpassword123",
            "mode_id": inserted_mode["_id"],
            "score": 200,
        }

        response = client.patch("/api/v1/users/", json=user_data)

        assert response.status_code == 404

    def test_modify_user_not_found_returns_correct_code(
        self,
        app: Flask,
        client: FlaskClient,
        mongo_db: Database,
        inserted_mode: dict[str, Any],
    ) -> None:
        mongo_db.users.delete_many({})

        user_data = {
            "username": "nonexistentuser",
            "password": "testpassword123",
            "mode_id": inserted_mode["_id"],
            "score": 200,
        }

        response = client.patch("/api/v1/users/", json=user_data)
        data = response.get_json()

        assert data["code"] == CODE_NOT_FOUND_USER

    def test_modify_user_wrong_password_returns_401(
        self,
        client: FlaskClient,
        inserted_user: dict[str, Any],
        inserted_mode: dict[str, Any],
    ) -> None:
        user_data = {
            "username": inserted_user["username"],
            "password": "wrongpassword",
            "mode_id": inserted_mode["_id"],
            "score": 200,
        }

        response = client.patch("/api/v1/users/", json=user_data)

        assert response.status_code == 401

    def test_modify_user_wrong_password_returns_correct_code(
        self,
        client: FlaskClient,
        inserted_user: dict[str, Any],
        inserted_mode: dict[str, Any],
    ) -> None:
        user_data = {
            "username": inserted_user["username"],
            "password": "wrongpassword",
            "mode_id": inserted_mode["_id"],
            "score": 200,
        }

        response = client.patch("/api/v1/users/", json=user_data)
        data = response.get_json()

        assert data["code"] == CODE_ERROR_AUTHENTICATION


class TestDeleteUserEndpoint:
    def test_delete_user_returns_200(
        self, client: FlaskClient, inserted_user: dict[str, Any]
    ) -> None:
        response = client.delete(f"/api/v1/users/{inserted_user['_id']}")

        assert response.status_code == 200

    def test_delete_user_returns_correct_structure(
        self, client: FlaskClient, inserted_user: dict[str, Any]
    ) -> None:
        response = client.delete(f"/api/v1/users/{inserted_user['_id']}")
        data = response.get_json()

        assert "code" in data
        assert "message" in data

    def test_delete_user_returns_correct_code(
        self, client: FlaskClient, inserted_user: dict[str, Any]
    ) -> None:
        response = client.delete(f"/api/v1/users/{inserted_user['_id']}")
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_DELETE_USER

    def test_delete_user_removes_from_database(
        self, client: FlaskClient, inserted_user: dict[str, Any], mongo_db: Database
    ) -> None:
        initial_count = mongo_db.users.count_documents({})

        client.delete(f"/api/v1/users/{inserted_user['_id']}")

        final_count = mongo_db.users.count_documents({})
        assert final_count == initial_count - 1

    def test_delete_nonexistent_user_returns_404(
        self, app: Flask, client: FlaskClient, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})
        fake_id = str(ObjectId())

        response = client.delete(f"/api/v1/users/{fake_id}")

        assert response.status_code == 404

    def test_delete_nonexistent_user_returns_correct_code(
        self, app: Flask, client: FlaskClient, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})
        fake_id = str(ObjectId())

        response = client.delete(f"/api/v1/users/{fake_id}")
        data = response.get_json()

        assert data["code"] == CODE_NOT_FOUND_USER
