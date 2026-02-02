from typing import Any

from bson import ObjectId
from flask import Flask
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult

from src.data_access.mode_dao import ModeDAO


class TestModeDAOInsert:
    def test_insert_one_creates_document(
        self, app: Flask, mongo_db: Database, sample_mode: dict[str, Any]
    ) -> None:
        mongo_db.modes.delete_many({})

        result = ModeDAO.insert_one(sample_mode.copy())

        assert result.inserted_id is not None

        doc = mongo_db.modes.find_one({"_id": result.inserted_id})
        assert doc is not None
        assert doc["name"] == sample_mode["name"]

    def test_insert_one_returns_insert_result(
        self, app: Flask, mongo_db: Database, sample_mode: dict[str, Any]
    ) -> None:
        mongo_db.modes.delete_many({})

        result = ModeDAO.insert_one(sample_mode.copy())

        assert isinstance(result, InsertOneResult)
        assert result.acknowledged is True

    def test_insert_multiple_documents(
        self, app: Flask, mongo_db: Database, sample_modes: list[dict[str, Any]]
    ) -> None:
        mongo_db.modes.delete_many({})

        for mode in sample_modes:
            ModeDAO.insert_one(mode.copy())

        count = mongo_db.modes.count_documents({})
        assert count == len(sample_modes)


class TestModeDAOFind:
    def test_find_returns_empty_list_when_no_documents(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})

        result = ModeDAO.find()

        assert result == []

    def test_find_returns_all_documents(
        self, app: Flask, inserted_modes: list[dict[str, Any]]
    ) -> None:
        result = ModeDAO.find()

        assert len(result) == len(inserted_modes)

    def test_find_returns_parsed_documents(
        self, app: Flask, inserted_modes: list[dict[str, Any]]
    ) -> None:
        result = ModeDAO.find()

        assert len(result) > 0
        assert all(isinstance(doc["_id"], str) for doc in result)


class TestModeDAOFindOneById:
    def test_find_one_by_id_returns_document(
        self, app: Flask, inserted_mode: dict[str, Any]
    ) -> None:
        result = ModeDAO.find_one_by_id(inserted_mode["_id"])

        assert result is not None
        assert result["_id"] == inserted_mode["_id"]
        assert result["name"] == inserted_mode["name"]

    def test_find_one_by_id_returns_none_for_nonexistent(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})
        fake_id = str(ObjectId())

        result = ModeDAO.find_one_by_id(fake_id)

        assert result is None

    def test_find_one_by_id_accepts_string_id(
        self, app: Flask, inserted_mode: dict[str, Any]
    ) -> None:
        result = ModeDAO.find_one_by_id(inserted_mode["_id"])

        assert result is not None
        assert isinstance(result["_id"], str)

    def test_find_one_by_id_returns_all_fields(
        self, app: Flask, inserted_mode: dict[str, Any]
    ) -> None:
        result = ModeDAO.find_one_by_id(inserted_mode["_id"])

        assert "name" in result
        assert "description" in result
        assert "multiplier" in result
        assert "timeleft" in result


class TestModeDAOFindOneByName:
    def test_find_one_by_name_returns_document(
        self, app: Flask, inserted_mode: dict[str, Any]
    ) -> None:
        result = ModeDAO.find_one_by_name(inserted_mode["name"])

        assert result is not None
        assert result["name"] == inserted_mode["name"]

    def test_find_one_by_name_is_case_insensitive(
        self, app: Flask, inserted_mode: dict[str, Any]
    ) -> None:
        result_lower = ModeDAO.find_one_by_name(inserted_mode["name"].lower())
        result_upper = ModeDAO.find_one_by_name(inserted_mode["name"].upper())

        assert result_lower is not None
        assert result_upper is not None
        assert result_lower["name"] == result_upper["name"]

    def test_find_one_by_name_returns_none_for_nonexistent(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})

        result = ModeDAO.find_one_by_name("NonexistentMode")

        assert result is None


class TestModeDAODelete:
    def test_delete_one_by_id_removes_document(
        self, app: Flask, inserted_mode: dict[str, Any], mongo_db: Database
    ) -> None:
        initial_count = mongo_db.modes.count_documents({})

        result = ModeDAO.delete_one_by_id(inserted_mode["_id"])

        assert result.deleted_count == 1
        assert mongo_db.modes.count_documents({}) == initial_count - 1

    def test_delete_one_by_id_returns_delete_result(
        self, app: Flask, inserted_mode: dict[str, Any]
    ) -> None:
        result = ModeDAO.delete_one_by_id(inserted_mode["_id"])

        assert isinstance(result, DeleteResult)
        assert result.acknowledged is True

    def test_delete_one_by_id_nonexistent_returns_zero(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})
        fake_id = str(ObjectId())

        result = ModeDAO.delete_one_by_id(fake_id)

        assert result.deleted_count == 0


class TestModeDAOParsing:
    def test_parse_mode_converts_id_to_string(self, app: Flask) -> None:
        doc = {
            "_id": ObjectId(),
            "name": "Test",
            "description": "Test description",
            "multiplier": 10,
            "timeleft": 90,
        }

        result = ModeDAO.parse_mode(doc)

        assert isinstance(result["_id"], str)

    def test_parse_mode_preserves_other_fields(self, app: Flask) -> None:
        doc = {
            "_id": ObjectId(),
            "name": "Test",
            "description": "Test description",
            "multiplier": 10,
            "timeleft": 90,
        }

        result = ModeDAO.parse_mode(doc)

        assert result["name"] == "Test"
        assert result["description"] == "Test description"
        assert result["multiplier"] == 10
        assert result["timeleft"] == 90

    def test_parse_mode_returns_none_for_none(self, app: Flask) -> None:
        result = ModeDAO.parse_mode(None)

        assert result is None

    def test_parse_modes_handles_list(self, app: Flask) -> None:
        docs = [
            {
                "_id": ObjectId(),
                "name": "Mode1",
                "description": "Desc1",
                "multiplier": 10,
                "timeleft": 90,
            },
            {
                "_id": ObjectId(),
                "name": "Mode2",
                "description": "Desc2",
                "multiplier": 100,
                "timeleft": 60,
            },
        ]

        result = ModeDAO.parse_modes(docs)

        assert len(result) == 2
        assert all(isinstance(doc["_id"], str) for doc in result)

    def test_parse_modes_handles_empty_list(self, app: Flask) -> None:
        result = ModeDAO.parse_modes([])

        assert result == []
