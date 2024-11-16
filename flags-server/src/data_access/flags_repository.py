from typing import Any
from bson import ObjectId

from flask import current_app


class FlagRepository:
    @staticmethod
    def get_all_flags() -> list[dict[str, Any]]:
        return list(current_app.mongo.db.flags.find())
    
    @staticmethod
    def get_flag(flag_id: ObjectId) -> dict[str, Any]:
        return current_app.mongo.db.flags.find_one({"_id": flag_id})

    @staticmethod
    def insert_flag(flag: dict[str, Any]) -> str:
        result = current_app.mongo.db.flags.insert_one(flag)
        return str(result.inserted_id)

    @staticmethod
    def get_random_flags(quantity: int) -> list[dict[str, Any]]:
        return list(current_app.mongo.db.flags.aggregate([{"$sample": {"size": quantity}}]))

    @staticmethod
    def delete_flag_by_id(flag_id: ObjectId) -> bool:
        result = current_app.mongo.db.flags.delete_one({"_id": flag_id})
        return bool(result.deleted_count)
