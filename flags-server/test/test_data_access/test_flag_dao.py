from bson import ObjectId
from flask import Flask
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult

from src.data_access.flag_dao import FlagDAO


class TestFlagDAOInsert:
    def test_insert_one_creates_document(
        self, app: Flask, mongo_db: Database, sample_flag: dict[str, str]
    ) -> None:
        mongo_db.flags.delete_many({})

        result = FlagDAO.insert_one(sample_flag.copy())

        assert result.inserted_id is not None

        doc = mongo_db.flags.find_one({"_id": result.inserted_id})
        assert doc is not None
        assert doc["name"] == sample_flag["name"]

    def test_insert_one_returns_insert_result(
        self, app: Flask, mongo_db: Database, sample_flag: dict[str, str]
    ) -> None:
        mongo_db.flags.delete_many({})

        result = FlagDAO.insert_one(sample_flag.copy())

        assert isinstance(result, InsertOneResult)
        assert result.acknowledged is True

    def test_insert_multiple_documents(
        self, app: Flask, mongo_db: Database, sample_flags: list[dict[str, str]]
    ) -> None:
        mongo_db.flags.delete_many({})

        for flag in sample_flags:
            FlagDAO.insert_one(flag.copy())

        count = mongo_db.flags.count_documents({})
        assert count == len(sample_flags)


class TestFlagDAOFind:
    def test_find_returns_empty_list_when_no_documents(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.flags.delete_many({})

        result = FlagDAO.find()

        assert result == []

    def test_find_returns_all_documents(
        self, app: Flask, inserted_flags: list[dict[str, str]]
    ) -> None:
        result = FlagDAO.find()

        assert len(result) == len(inserted_flags)

    def test_find_returns_parsed_documents(
        self, app: Flask, inserted_flags: list[dict[str, str]]
    ) -> None:
        result = FlagDAO.find()

        assert len(result) > 0
        assert all(isinstance(doc["_id"], str) for doc in result)


class TestFlagDAOFindRandom:
    def test_find_random_returns_requested_quantity(
        self, app: Flask, inserted_flags: list[dict[str, str]]
    ) -> None:
        result = FlagDAO.find_random(2)

        assert len(result) == 2

    def test_find_random_returns_parsed_documents(
        self, app: Flask, inserted_flags: list[dict[str, str]]
    ) -> None:
        result = FlagDAO.find_random(2)

        assert all(isinstance(doc["_id"], str) for doc in result)

    def test_find_random_returns_empty_when_no_documents(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.flags.delete_many({})

        result = FlagDAO.find_random(5)

        assert result == []

    def test_find_random_returns_all_when_quantity_exceeds_total(
        self, app: Flask, inserted_flags: list[dict[str, str]]
    ) -> None:
        result = FlagDAO.find_random(100)

        assert len(result) == len(inserted_flags)


class TestFlagDAOFindOneById:
    def test_find_one_by_id_returns_document(
        self, app: Flask, inserted_flag: dict[str, str]
    ) -> None:
        result = FlagDAO.find_one_by_id(inserted_flag["_id"])

        assert result is not None
        assert result["_id"] == inserted_flag["_id"]
        assert result["name"] == inserted_flag["name"]

    def test_find_one_by_id_returns_none_for_nonexistent(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.flags.delete_many({})
        fake_id = str(ObjectId())

        result = FlagDAO.find_one_by_id(fake_id)

        assert result is None

    def test_find_one_by_id_accepts_string_id(
        self, app: Flask, inserted_flag: dict[str, str]
    ) -> None:
        result = FlagDAO.find_one_by_id(inserted_flag["_id"])

        assert result is not None
        assert isinstance(result["_id"], str)


class TestFlagDAOFindOneByName:
    def test_find_one_by_name_returns_document(
        self, app: Flask, inserted_flag: dict[str, str]
    ) -> None:
        result = FlagDAO.find_one_by_name(inserted_flag["name"])

        assert result is not None
        assert result["name"] == inserted_flag["name"]

    def test_find_one_by_name_is_case_insensitive(
        self, app: Flask, inserted_flag: dict[str, str]
    ) -> None:
        result_lower = FlagDAO.find_one_by_name(inserted_flag["name"].lower())
        result_upper = FlagDAO.find_one_by_name(inserted_flag["name"].upper())

        assert result_lower is not None
        assert result_upper is not None
        assert result_lower["name"] == result_upper["name"]

    def test_find_one_by_name_returns_none_for_nonexistent(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.flags.delete_many({})

        result = FlagDAO.find_one_by_name("NonexistentFlag")

        assert result is None


class TestFlagDAODelete:
    def test_delete_one_by_id_removes_document(
        self, app: Flask, inserted_flag: dict[str, str], mongo_db: Database
    ) -> None:
        initial_count = mongo_db.flags.count_documents({})

        result = FlagDAO.delete_one_by_id(inserted_flag["_id"])

        assert result.deleted_count == 1
        assert mongo_db.flags.count_documents({}) == initial_count - 1

    def test_delete_one_by_id_returns_delete_result(
        self, app: Flask, inserted_flag: dict[str, str]
    ) -> None:
        result = FlagDAO.delete_one_by_id(inserted_flag["_id"])

        assert isinstance(result, DeleteResult)
        assert result.acknowledged is True

    def test_delete_one_by_id_nonexistent_returns_zero(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.flags.delete_many({})
        fake_id = str(ObjectId())

        result = FlagDAO.delete_one_by_id(fake_id)

        assert result.deleted_count == 0


class TestFlagDAOParsing:
    def test_parse_flag_converts_id_to_string(self, app: Flask) -> None:
        doc = {
            "_id": ObjectId(),
            "name": "Test",
            "image": "https://example.com/test.png",
        }

        result = FlagDAO.parse_flag(doc)

        assert isinstance(result["_id"], str)

    def test_parse_flag_preserves_other_fields(self, app: Flask) -> None:
        doc = {
            "_id": ObjectId(),
            "name": "Test",
            "image": "https://example.com/test.png",
        }

        result = FlagDAO.parse_flag(doc)

        assert result["name"] == "Test"
        assert result["image"] == "https://example.com/test.png"

    def test_parse_flag_returns_none_for_none(self, app: Flask) -> None:
        result = FlagDAO.parse_flag(None)

        assert result is None

    def test_parse_flags_handles_list(self, app: Flask) -> None:
        docs = [
            {"_id": ObjectId(), "name": "Flag1", "image": "https://example.com/1.png"},
            {"_id": ObjectId(), "name": "Flag2", "image": "https://example.com/2.png"},
        ]

        result = FlagDAO.parse_flags(docs)

        assert len(result) == 2
        assert all(isinstance(doc["_id"], str) for doc in result)

    def test_parse_flags_handles_empty_list(self, app: Flask) -> None:
        result = FlagDAO.parse_flags([])

        assert result == []
