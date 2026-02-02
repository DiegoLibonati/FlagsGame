from flask import Flask
from pymongo.database import Database

from src.constants.defaults import DEFAULT_FLAGS
from src.startup.init_flags import add_default_flags


class TestAddDefaultFlags:
    def test_adds_flags_when_empty(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.flags.delete_many({})

        add_default_flags()

        count = mongo_db.flags.count_documents({})
        assert count == len(DEFAULT_FLAGS)

    def test_does_not_add_when_flags_exist(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.flags.delete_many({})
        mongo_db.flags.insert_one(
            {"name": "ExistingFlag", "image": "https://example.com/flag.png"}
        )

        add_default_flags()

        count = mongo_db.flags.count_documents({})
        assert count == 1

    def test_adds_correct_flag_names(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.flags.delete_many({})

        add_default_flags()

        expected_names = [flag["name"] for flag in DEFAULT_FLAGS]
        actual_names = [flag["name"] for flag in mongo_db.flags.find()]

        for name in expected_names:
            assert name in actual_names

    def test_adds_correct_flag_images(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.flags.delete_many({})

        add_default_flags()

        expected_images = [flag["image"] for flag in DEFAULT_FLAGS]
        actual_images = [flag["image"] for flag in mongo_db.flags.find()]

        for image in expected_images:
            assert image in actual_images

    def test_is_idempotent(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.flags.delete_many({})

        add_default_flags()
        initial_count = mongo_db.flags.count_documents({})

        add_default_flags()
        final_count = mongo_db.flags.count_documents({})

        assert initial_count == final_count
