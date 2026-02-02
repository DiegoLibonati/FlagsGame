import pytest
from bson import ObjectId
from flask import Flask
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult

from src.constants.codes import CODE_ERROR_FLAG_ALREADY_EXISTS, CODE_NOT_FOUND_FLAG
from src.models.flag_model import FlagModel
from src.services.flag_service import FlagService
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


class TestFlagServiceAddFlag:
    def test_add_flag_inserts_document(
        self, app: Flask, mongo_db: Database, sample_flag: dict[str, str]
    ) -> None:
        mongo_db.flags.delete_many({})

        flag = FlagModel(**sample_flag)
        result = FlagService.add_flag(flag)

        assert result.inserted_id is not None

        doc = mongo_db.flags.find_one({"_id": result.inserted_id})
        assert doc is not None
        assert doc["name"] == sample_flag["name"]

    def test_add_flag_returns_insert_result(
        self, app: Flask, mongo_db: Database, sample_flag: dict[str, str]
    ) -> None:
        mongo_db.flags.delete_many({})

        flag = FlagModel(**sample_flag)
        result = FlagService.add_flag(flag)

        assert isinstance(result, InsertOneResult)

    def test_add_flag_raises_conflict_for_duplicate(
        self, app: Flask, inserted_flag: dict[str, str]
    ) -> None:
        flag = FlagModel(
            name=inserted_flag["name"], image="https://example.com/other.png"
        )

        with pytest.raises(ConflictAPIError) as exc_info:
            FlagService.add_flag(flag)

        assert exc_info.value.status_code == 409
        assert exc_info.value.code == CODE_ERROR_FLAG_ALREADY_EXISTS

    def test_add_flag_duplicate_is_case_insensitive(
        self, app: Flask, inserted_flag: dict[str, str]
    ) -> None:
        flag = FlagModel(
            name=inserted_flag["name"].upper(), image="https://example.com/other.png"
        )

        with pytest.raises(ConflictAPIError):
            FlagService.add_flag(flag)


class TestFlagServiceGetAllFlags:
    def test_get_all_flags_returns_empty_list(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.flags.delete_many({})

        result = FlagService.get_all_flags()

        assert result == []

    def test_get_all_flags_returns_all(
        self, app: Flask, inserted_flags: list[dict[str, str]]
    ) -> None:
        result = FlagService.get_all_flags()

        assert len(result) == len(inserted_flags)

    def test_get_all_flags_returns_parsed_documents(
        self, app: Flask, inserted_flags: list[dict[str, str]]
    ) -> None:
        result = FlagService.get_all_flags()

        assert len(result) > 0
        assert all(isinstance(doc["_id"], str) for doc in result)


class TestFlagServiceGetRandomFlags:
    def test_get_random_flags_returns_requested_quantity(
        self, app: Flask, inserted_flags: list[dict[str, str]]
    ) -> None:
        result = FlagService.get_random_flags(2)

        assert len(result) == 2

    def test_get_random_flags_returns_empty_when_no_flags(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.flags.delete_many({})

        result = FlagService.get_random_flags(5)

        assert result == []

    def test_get_random_flags_returns_all_when_quantity_exceeds_total(
        self, app: Flask, inserted_flags: list[dict[str, str]]
    ) -> None:
        result = FlagService.get_random_flags(100)

        assert len(result) == len(inserted_flags)

    def test_get_random_flags_returns_parsed_documents(
        self, app: Flask, inserted_flags: list[dict[str, str]]
    ) -> None:
        result = FlagService.get_random_flags(2)

        assert all(isinstance(doc["_id"], str) for doc in result)


class TestFlagServiceDeleteFlagById:
    def test_delete_flag_removes_document(
        self, app: Flask, inserted_flag: dict[str, str], mongo_db: Database
    ) -> None:
        initial_count = mongo_db.flags.count_documents({})

        FlagService.delete_flag_by_id(inserted_flag["_id"])

        final_count = mongo_db.flags.count_documents({})
        assert final_count == initial_count - 1

    def test_delete_flag_returns_delete_result(
        self, app: Flask, inserted_flag: dict[str, str]
    ) -> None:
        result = FlagService.delete_flag_by_id(inserted_flag["_id"])

        assert isinstance(result, DeleteResult)

    def test_delete_flag_raises_not_found(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.flags.delete_many({})
        fake_id = str(ObjectId())

        with pytest.raises(NotFoundAPIError) as exc_info:
            FlagService.delete_flag_by_id(fake_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == CODE_NOT_FOUND_FLAG

    def test_delete_flag_only_removes_one(
        self, app: Flask, inserted_flags: list[dict[str, str]], mongo_db: Database
    ) -> None:
        initial_count = mongo_db.flags.count_documents({})

        FlagService.delete_flag_by_id(inserted_flags[0]["_id"])

        final_count = mongo_db.flags.count_documents({})
        assert final_count == initial_count - 1


class TestFlagServiceIntegration:
    def test_full_crud_cycle(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.flags.delete_many({})

        flag = FlagModel(name="TestFlag", image="https://example.com/test.png")
        create_result = FlagService.add_flag(flag)
        flag_id = str(create_result.inserted_id)

        flags = FlagService.get_all_flags()
        assert len(flags) == 1
        assert flags[0]["_id"] == flag_id

        delete_result = FlagService.delete_flag_by_id(flag_id)
        assert delete_result.deleted_count == 1

        flags = FlagService.get_all_flags()
        assert len(flags) == 0
