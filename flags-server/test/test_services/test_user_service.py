from typing import Any

import pytest
from bson import ObjectId
from flask import Flask
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from src.constants.codes import CODE_ERROR_USER_ALREADY_EXISTS, CODE_NOT_FOUND_USER
from src.models.user_model import UserModel
from src.services.user_service import UserService
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


class TestUserServiceAddUser:
    def test_add_user_inserts_document(
        self, app: Flask, mongo_db: Database, sample_user: dict[str, Any]
    ) -> None:
        mongo_db.users.delete_many({})

        user = UserModel(**sample_user)
        result = UserService.add_user(user)

        assert result.inserted_id is not None

        doc = mongo_db.users.find_one({"_id": result.inserted_id})
        assert doc is not None
        assert doc["username"] == sample_user["username"]

    def test_add_user_returns_insert_result(
        self, app: Flask, mongo_db: Database, sample_user: dict[str, Any]
    ) -> None:
        mongo_db.users.delete_many({})

        user = UserModel(**sample_user)
        result = UserService.add_user(user)

        assert isinstance(result, InsertOneResult)

    def test_add_user_raises_conflict_for_duplicate(
        self, app: Flask, inserted_user: dict[str, Any]
    ) -> None:
        user = UserModel(
            username=inserted_user["username"],
            password="otherpassword",
            scores={},
            total_score=0,
        )

        with pytest.raises(ConflictAPIError) as exc_info:
            UserService.add_user(user)

        assert exc_info.value.status_code == 409
        assert exc_info.value.code == CODE_ERROR_USER_ALREADY_EXISTS


class TestUserServiceGetAllUsers:
    def test_get_all_users_returns_empty_list(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})

        result = UserService.get_all_users()

        assert result == []

    def test_get_all_users_returns_all(
        self, app: Flask, inserted_users: list[dict[str, Any]]
    ) -> None:
        result = UserService.get_all_users()

        assert len(result) == len(inserted_users)

    def test_get_all_users_returns_parsed_documents(
        self, app: Flask, inserted_users: list[dict[str, Any]]
    ) -> None:
        result = UserService.get_all_users()

        assert len(result) > 0
        assert all(isinstance(doc["_id"], str) for doc in result)


class TestUserServiceGetUserByUsername:
    def test_get_user_by_username_returns_document(
        self, app: Flask, inserted_user: dict[str, Any]
    ) -> None:
        result = UserService.get_user_by_username(inserted_user["username"])

        assert result is not None
        assert result["username"] == inserted_user["username"]

    def test_get_user_by_username_returns_none_for_nonexistent(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})

        result = UserService.get_user_by_username("nonexistentuser")

        assert result is None

    def test_get_user_by_username_is_case_sensitive(
        self, app: Flask, inserted_user: dict[str, Any]
    ) -> None:
        result = UserService.get_user_by_username(inserted_user["username"].upper())

        assert result is None


class TestUserServiceGetTopUsers:
    def test_get_top_users_returns_empty_when_no_users(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})

        result = UserService.get_top_users("General")

        assert result == []

    def test_get_top_users_returns_sorted_by_general_score(
        self, app: Flask, inserted_users: list[dict[str, Any]]
    ) -> None:
        result = UserService.get_top_users("General")

        scores = [user["score"] for user in result]
        assert scores == sorted(scores, reverse=True)

    def test_get_top_users_returns_max_10(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.users.delete_many({})

        for i in range(15):
            mongo_db.users.insert_one(
                {
                    "username": f"user{i}",
                    "password": "pass",
                    "scores": {"General": i * 10},
                    "total_score": i * 10,
                }
            )

        result = UserService.get_top_users("General")

        assert len(result) == 10

    def test_get_top_users_uses_total_score_for_general(
        self, app: Flask, inserted_users: list[dict[str, Any]]
    ) -> None:
        result = UserService.get_top_users("General")

        assert len(result) > 0
        assert all("score" in user for user in result)

    def test_get_top_users_uses_mode_score_for_specific_mode(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})

        mongo_db.users.insert_one(
            {
                "username": "user1",
                "password": "pass",
                "scores": {"General": 100, "Normal": 50},
                "total_score": 100,
            }
        )
        mongo_db.users.insert_one(
            {
                "username": "user2",
                "password": "pass",
                "scores": {"General": 50, "Normal": 200},
                "total_score": 50,
            }
        )

        result = UserService.get_top_users("Normal")

        assert result[0]["username"] == "user2"
        assert result[0]["score"] == 200

    def test_get_top_users_returns_zero_for_missing_mode(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})

        mongo_db.users.insert_one(
            {
                "username": "user1",
                "password": "pass",
                "scores": {"General": 100},
                "total_score": 100,
            }
        )

        result = UserService.get_top_users("NonexistentMode")

        assert result[0]["score"] == 0


class TestUserServiceUpdateUserScoresByUsername:
    def test_update_user_scores_updates_document(
        self, app: Flask, inserted_user: dict[str, Any], mongo_db: Database
    ) -> None:
        new_scores = {"General": 500, "Normal": 300}

        UserService.update_user_scores_by_username(
            inserted_user["username"], {"scores": new_scores}
        )

        doc = mongo_db.users.find_one({"username": inserted_user["username"]})
        assert doc["scores"] == new_scores

    def test_update_user_scores_returns_update_result(
        self, app: Flask, inserted_user: dict[str, Any]
    ) -> None:
        result = UserService.update_user_scores_by_username(
            inserted_user["username"], {"total_score": 999}
        )

        assert isinstance(result, UpdateResult)

    def test_update_user_scores_updates_total_score(
        self, app: Flask, inserted_user: dict[str, Any], mongo_db: Database
    ) -> None:
        UserService.update_user_scores_by_username(
            inserted_user["username"], {"total_score": 999}
        )

        doc = mongo_db.users.find_one({"username": inserted_user["username"]})
        assert doc["total_score"] == 999


class TestUserServiceDeleteUserById:
    def test_delete_user_removes_document(
        self, app: Flask, inserted_user: dict[str, Any], mongo_db: Database
    ) -> None:
        initial_count = mongo_db.users.count_documents({})

        UserService.delete_user_by_id(inserted_user["_id"])

        final_count = mongo_db.users.count_documents({})
        assert final_count == initial_count - 1

    def test_delete_user_returns_delete_result(
        self, app: Flask, inserted_user: dict[str, Any]
    ) -> None:
        result = UserService.delete_user_by_id(inserted_user["_id"])

        assert isinstance(result, DeleteResult)

    def test_delete_user_raises_not_found(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.users.delete_many({})
        fake_id = str(ObjectId())

        with pytest.raises(NotFoundAPIError) as exc_info:
            UserService.delete_user_by_id(fake_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == CODE_NOT_FOUND_USER

    def test_delete_user_only_removes_one(
        self, app: Flask, inserted_users: list[dict[str, Any]], mongo_db: Database
    ) -> None:
        initial_count = mongo_db.users.count_documents({})

        UserService.delete_user_by_id(inserted_users[0]["_id"])

        final_count = mongo_db.users.count_documents({})
        assert final_count == initial_count - 1


class TestUserServiceIntegration:
    def test_full_crud_cycle(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.users.delete_many({})

        user = UserModel(
            username="integrationuser",
            password="integrationpass",
            scores={"General": 100},
            total_score=100,
        )
        create_result = UserService.add_user(user)
        user_id = str(create_result.inserted_id)

        users = UserService.get_all_users()
        assert len(users) == 1

        found_user = UserService.get_user_by_username("integrationuser")
        assert found_user is not None

        UserService.update_user_scores_by_username(
            "integrationuser", {"total_score": 500}
        )
        updated_user = UserService.get_user_by_username("integrationuser")
        assert updated_user["total_score"] == 500

        delete_result = UserService.delete_user_by_id(user_id)
        assert delete_result.deleted_count == 1

        users = UserService.get_all_users()
        assert len(users) == 0
