from typing import Any
from bson import ObjectId

from flask import current_app


class ModeRepository:
    @staticmethod
    def get_all_modes() -> list[dict[str, Any]]:
        return list(current_app.mongo.db.modes.find())

    @staticmethod
    def get_mode_by_name(name: str) -> dict[str, Any]:
        return current_app.mongo.db.modes.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
    
    @staticmethod
    def get_mode_by_id(mode_id: ObjectId) -> dict[str, Any]:
        return current_app.mongo.db.modes.find_one({"_id": mode_id})
    
    @staticmethod
    def insert_mode(mode: dict[str, Any]) -> str:
        result = current_app.mongo.db.modes.insert_one(mode)
        return str(result.inserted_id)

    @staticmethod
    def delete_mode_by_id(mode_id: ObjectId) -> bool:
        result = current_app.mongo.db.modes.delete_one({"_id": mode_id})
        return bool(result.deleted_count)
