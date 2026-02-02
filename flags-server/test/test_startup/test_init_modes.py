from flask import Flask
from pymongo.database import Database

from src.constants.defaults import DEFAULT_MODES
from src.startup.init_modes import add_default_modes


class TestAddDefaultModes:
    def test_adds_modes_when_empty(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.modes.delete_many({})

        add_default_modes()

        count = mongo_db.modes.count_documents({})
        assert count == len(DEFAULT_MODES)

    def test_does_not_add_when_modes_exist(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.modes.delete_many({})
        mongo_db.modes.insert_one(
            {
                "name": "ExistingMode",
                "description": "Existing mode",
                "multiplier": 10,
                "timeleft": 90,
            }
        )

        add_default_modes()

        count = mongo_db.modes.count_documents({})
        assert count == 1

    def test_adds_correct_mode_names(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.modes.delete_many({})

        add_default_modes()

        expected_names = [mode["name"] for mode in DEFAULT_MODES]
        actual_names = [mode["name"] for mode in mongo_db.modes.find()]

        for name in expected_names:
            assert name in actual_names

    def test_adds_correct_mode_data(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.modes.delete_many({})

        add_default_modes()

        for default_mode in DEFAULT_MODES:
            doc = mongo_db.modes.find_one({"name": default_mode["name"]})
            assert doc is not None
            assert doc["description"] == default_mode["description"]
            assert doc["multiplier"] == default_mode["multiplier"]
            assert doc["timeleft"] == default_mode["timeleft"]

    def test_is_idempotent(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.modes.delete_many({})

        add_default_modes()
        initial_count = mongo_db.modes.count_documents({})

        add_default_modes()
        final_count = mongo_db.modes.count_documents({})

        assert initial_count == final_count
