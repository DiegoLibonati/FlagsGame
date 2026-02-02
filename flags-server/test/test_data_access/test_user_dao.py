from typing import Any

from bson import ObjectId
from flask import Flask
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from src.data_access.user_dao import UserDAO


class TestUserDAOInsert:
    def test_insert_one_creates_document(
        self, app: Flask, mongo_db: Database, sample_user: dict[str, Any]
    ) -> None:
        mongo_db.users.delete_many({})

        result = UserDAO.insert_one(sample_user.copy())

        assert result.inserted_id is not None

        doc = mongo_db.users.find_one({"_id": result.inserted_id})
        assert doc is not None
        assert doc["username"] == sample_user["username"]

    def test_insert_one_returns_insert_result(
        self, app: Flask, mongo_db: Database, sample_user: dict[str, Any]
    ) -> None:
        mongo_db.users.delete_many({})

        result = UserDAO.insert_one(sample_user.copy())

        assert isinstance(result, InsertOneResult)
        assert result.acknowledged is True

    def test_insert_multiple_documents(
        self, app: Flask, mongo_db: Database, sample_users: list[dict[str, Any]]
    ) -> None:
        mongo_db.users.delete_many({})

        for user in sample_users:
            UserDAO.insert_one(user.copy())

        count = mongo_db.users.count_documents({})
        assert count == len(sample_users)


class TestUserDAOFind:
    def test_find_returns_empty_list_when_no_documents(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})

        result = UserDAO.find()

        assert result == []

    def test_find_returns_all_documents(
        self, app: Flask, inserted_users: list[dict[str, Any]]
    ) -> None:
        result = UserDAO.find()

        assert len(result) == len(inserted_users)

    def test_find_returns_parsed_documents(
        self, app: Flask, inserted_users: list[dict[str, Any]]
    ) -> None:
        result = UserDAO.find()

        assert len(result) > 0
        assert all(isinstance(doc["_id"], str) for doc in result)


class TestUserDAOFindOneById:
    def test_find_one_by_id_returns_document(
        self, app: Flask, inserted_user: dict[str, Any]
    ) -> None:
        result = UserDAO.find_one_by_id(inserted_user["_id"])

        assert result is not None
        assert result["_id"] == inserted_user["_id"]
        assert result["username"] == inserted_user["username"]

    def test_find_one_by_id_returns_none_for_nonexistent(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})
        fake_id = str(ObjectId())

        result = UserDAO.find_one_by_id(fake_id)

        assert result is None

    def test_find_one_by_id_accepts_string_id(
        self, app: Flask, inserted_user: dict[str, Any]
    ) -> None:
        result = UserDAO.find_one_by_id(inserted_user["_id"])

        assert result is not None
        assert isinstance(result["_id"], str)

    def test_find_one_by_id_returns_all_fields(
        self, app: Flask, inserted_user: dict[str, Any]
    ) -> None:
        result = UserDAO.find_one_by_id(inserted_user["_id"])

        assert "username" in result
        assert "password" in result
        assert "scores" in result
        assert "total_score" in result


class TestUserDAOFindOneByUsername:
    def test_find_one_by_username_returns_document(
        self, app: Flask, inserted_user: dict[str, Any]
    ) -> None:
        result = UserDAO.find_one_by_username(inserted_user["username"])

        assert result is not None
        assert result["username"] == inserted_user["username"]

    def test_find_one_by_username_returns_none_for_nonexistent(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})

        result = UserDAO.find_one_by_username("nonexistentuser")

        assert result is None

    def test_find_one_by_username_is_case_sensitive(
        self, app: Flask, inserted_user: dict[str, Any]
    ) -> None:
        result_upper = UserDAO.find_one_by_username(inserted_user["username"].upper())

        assert result_upper is None


class TestUserDAOUpdateOneByUsername:
    def test_update_one_by_username_updates_document(
        self, app: Flask, inserted_user: dict[str, Any], mongo_db: Database
    ) -> None:
        new_score = 999

        UserDAO.update_one_by_username(
            inserted_user["username"], {"total_score": new_score}
        )

        doc = mongo_db.users.find_one({"username": inserted_user["username"]})
        assert doc["total_score"] == new_score

    def test_update_one_by_username_returns_update_result(
        self, app: Flask, inserted_user: dict[str, Any]
    ) -> None:
        result = UserDAO.update_one_by_username(
            inserted_user["username"], {"total_score": 500}
        )

        assert isinstance(result, UpdateResult)
        assert result.acknowledged is True

    def test_update_one_by_username_modifies_only_specified_fields(
        self, app: Flask, inserted_user: dict[str, Any], mongo_db: Database
    ) -> None:
        original_username = inserted_user["username"]

        UserDAO.update_one_by_username(original_username, {"total_score": 500})

        doc = mongo_db.users.find_one({"username": original_username})
        assert doc["username"] == original_username
        assert doc["total_score"] == 500

    def test_update_one_by_username_nonexistent_returns_zero_matched(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})

        result = UserDAO.update_one_by_username("nonexistentuser", {"total_score": 100})

        assert result.matched_count == 0

    def test_update_one_by_username_updates_nested_scores(
        self, app: Flask, inserted_user: dict[str, Any], mongo_db: Database
    ) -> None:
        new_scores = {"General": 500, "Normal": 300, "Hard": 200}

        UserDAO.update_one_by_username(
            inserted_user["username"], {"scores": new_scores}
        )

        doc = mongo_db.users.find_one({"username": inserted_user["username"]})
        assert doc["scores"] == new_scores


class TestUserDAODelete:
    def test_delete_one_by_id_removes_document(
        self, app: Flask, inserted_user: dict[str, Any], mongo_db: Database
    ) -> None:
        initial_count = mongo_db.users.count_documents({})

        result = UserDAO.delete_one_by_id(inserted_user["_id"])

        assert result.deleted_count == 1
        assert mongo_db.users.count_documents({}) == initial_count - 1

    def test_delete_one_by_id_returns_delete_result(
        self, app: Flask, inserted_user: dict[str, Any]
    ) -> None:
        result = UserDAO.delete_one_by_id(inserted_user["_id"])

        assert isinstance(result, DeleteResult)
        assert result.acknowledged is True

    def test_delete_one_by_id_nonexistent_returns_zero(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.users.delete_many({})
        fake_id = str(ObjectId())

        result = UserDAO.delete_one_by_id(fake_id)

        assert result.deleted_count == 0


class TestUserDAOParsing:
    def test_parse_user_converts_id_to_string(self, app: Flask) -> None:
        doc = {
            "_id": ObjectId(),
            "username": "testuser",
            "password": "hashedpassword",
            "scores": {"General": 100},
            "total_score": 100,
        }

        result = UserDAO.parse_user(doc)

        assert isinstance(result["_id"], str)

    def test_parse_user_preserves_other_fields(self, app: Flask) -> None:
        doc = {
            "_id": ObjectId(),
            "username": "testuser",
            "password": "hashedpassword",
            "scores": {"General": 100},
            "total_score": 100,
        }

        result = UserDAO.parse_user(doc)

        assert result["username"] == "testuser"
        assert result["password"] == "hashedpassword"
        assert result["scores"] == {"General": 100}
        assert result["total_score"] == 100

    def test_parse_user_returns_none_for_none(self, app: Flask) -> None:
        result = UserDAO.parse_user(None)

        assert result is None

    def test_parse_users_handles_list(self, app: Flask) -> None:
        docs = [
            {
                "_id": ObjectId(),
                "username": "user1",
                "password": "pass1",
                "scores": {},
                "total_score": 0,
            },
            {
                "_id": ObjectId(),
                "username": "user2",
                "password": "pass2",
                "scores": {},
                "total_score": 0,
            },
        ]

        result = UserDAO.parse_users(docs)

        assert len(result) == 2
        assert all(isinstance(doc["_id"], str) for doc in result)

    def test_parse_users_handles_empty_list(self, app: Flask) -> None:
        result = UserDAO.parse_users([])

        assert result == []
