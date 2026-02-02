from typing import Any

import pytest
from bson import ObjectId
from flask import Flask
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult

from src.constants.codes import CODE_ERROR_MODE_ALREADY_EXISTS, CODE_NOT_FOUND_MODE
from src.models.mode_model import ModeModel
from src.services.mode_service import ModeService
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


class TestModeServiceAddMode:
    def test_add_mode_inserts_document(
        self, app: Flask, mongo_db: Database, sample_mode: dict[str, Any]
    ) -> None:
        mongo_db.modes.delete_many({})

        mode = ModeModel(**sample_mode)
        result = ModeService.add_mode(mode)

        assert result.inserted_id is not None

        doc = mongo_db.modes.find_one({"_id": result.inserted_id})
        assert doc is not None
        assert doc["name"] == sample_mode["name"]

    def test_add_mode_returns_insert_result(
        self, app: Flask, mongo_db: Database, sample_mode: dict[str, Any]
    ) -> None:
        mongo_db.modes.delete_many({})

        mode = ModeModel(**sample_mode)
        result = ModeService.add_mode(mode)

        assert isinstance(result, InsertOneResult)

    def test_add_mode_raises_conflict_for_duplicate(
        self, app: Flask, inserted_mode: dict[str, Any]
    ) -> None:
        mode = ModeModel(
            name=inserted_mode["name"],
            description="Other description",
            multiplier=50,
            timeleft=45,
        )

        with pytest.raises(ConflictAPIError) as exc_info:
            ModeService.add_mode(mode)

        assert exc_info.value.status_code == 409
        assert exc_info.value.code == CODE_ERROR_MODE_ALREADY_EXISTS

    def test_add_mode_duplicate_is_case_insensitive(
        self, app: Flask, inserted_mode: dict[str, Any]
    ) -> None:
        mode = ModeModel(
            name=inserted_mode["name"].upper(),
            description="Other description",
            multiplier=50,
            timeleft=45,
        )

        with pytest.raises(ConflictAPIError):
            ModeService.add_mode(mode)


class TestModeServiceGetAllModes:
    def test_get_all_modes_returns_empty_list(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})

        result = ModeService.get_all_modes()

        assert result == []

    def test_get_all_modes_returns_all(
        self, app: Flask, inserted_modes: list[dict[str, Any]]
    ) -> None:
        result = ModeService.get_all_modes()

        assert len(result) == len(inserted_modes)

    def test_get_all_modes_returns_parsed_documents(
        self, app: Flask, inserted_modes: list[dict[str, Any]]
    ) -> None:
        result = ModeService.get_all_modes()

        assert len(result) > 0
        assert all(isinstance(doc["_id"], str) for doc in result)


class TestModeServiceGetModeById:
    def test_get_mode_by_id_returns_document(
        self, app: Flask, inserted_mode: dict[str, Any]
    ) -> None:
        result = ModeService.get_mode_by_id(inserted_mode["_id"])

        assert result is not None
        assert result["_id"] == inserted_mode["_id"]
        assert result["name"] == inserted_mode["name"]

    def test_get_mode_by_id_returns_none_for_nonexistent(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})
        fake_id = str(ObjectId())

        result = ModeService.get_mode_by_id(fake_id)

        assert result is None

    def test_get_mode_by_id_returns_all_fields(
        self, app: Flask, inserted_mode: dict[str, Any]
    ) -> None:
        result = ModeService.get_mode_by_id(inserted_mode["_id"])

        assert "name" in result
        assert "description" in result
        assert "multiplier" in result
        assert "timeleft" in result


class TestModeServiceGetModeByName:
    def test_get_mode_by_name_returns_document(
        self, app: Flask, inserted_mode: dict[str, Any]
    ) -> None:
        result = ModeService.get_mode_by_name(inserted_mode["name"])

        assert result is not None
        assert result["name"] == inserted_mode["name"]

    def test_get_mode_by_name_returns_none_for_nonexistent(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})

        result = ModeService.get_mode_by_name("NonexistentMode")

        assert result is None

    def test_get_mode_by_name_is_case_insensitive(
        self, app: Flask, inserted_mode: dict[str, Any]
    ) -> None:
        result_lower = ModeService.get_mode_by_name(inserted_mode["name"].lower())
        result_upper = ModeService.get_mode_by_name(inserted_mode["name"].upper())

        assert result_lower is not None
        assert result_upper is not None


class TestModeServiceDeleteModeById:
    def test_delete_mode_removes_document(
        self, app: Flask, inserted_mode: dict[str, Any], mongo_db: Database
    ) -> None:
        initial_count = mongo_db.modes.count_documents({})

        ModeService.delete_mode_by_id(inserted_mode["_id"])

        final_count = mongo_db.modes.count_documents({})
        assert final_count == initial_count - 1

    def test_delete_mode_returns_delete_result(
        self, app: Flask, inserted_mode: dict[str, Any]
    ) -> None:
        result = ModeService.delete_mode_by_id(inserted_mode["_id"])

        assert isinstance(result, DeleteResult)

    def test_delete_mode_raises_not_found(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.modes.delete_many({})
        fake_id = str(ObjectId())

        with pytest.raises(NotFoundAPIError) as exc_info:
            ModeService.delete_mode_by_id(fake_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == CODE_NOT_FOUND_MODE

    def test_delete_mode_only_removes_one(
        self, app: Flask, inserted_modes: list[dict[str, Any]], mongo_db: Database
    ) -> None:
        initial_count = mongo_db.modes.count_documents({})

        ModeService.delete_mode_by_id(inserted_modes[0]["_id"])

        final_count = mongo_db.modes.count_documents({})
        assert final_count == initial_count - 1


class TestModeServiceIntegration:
    def test_full_crud_cycle(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.modes.delete_many({})

        mode = ModeModel(
            name="TestMode",
            description="Test mode description",
            multiplier=50,
            timeleft=60,
        )
        create_result = ModeService.add_mode(mode)
        mode_id = str(create_result.inserted_id)

        modes = ModeService.get_all_modes()
        assert len(modes) == 1
        assert modes[0]["_id"] == mode_id

        found_mode = ModeService.get_mode_by_id(mode_id)
        assert found_mode is not None
        assert found_mode["name"] == "TestMode"

        delete_result = ModeService.delete_mode_by_id(mode_id)
        assert delete_result.deleted_count == 1

        modes = ModeService.get_all_modes()
        assert len(modes) == 0
