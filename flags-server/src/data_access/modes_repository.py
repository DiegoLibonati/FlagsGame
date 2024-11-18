from typing import Any
from bson import ObjectId

from flask_pymongo.wrappers import Database


class ModeRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def get_all_modes(self) -> list[dict[str, Any]]:
        return list(self.db.modes.find())

    def get_mode_by_name(self, name: str) -> dict[str, Any]:
        return self.db.modes.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
    
    def get_mode_by_id(self, mode_id: ObjectId) -> dict[str, Any]:
        return self.db.modes.find_one({"_id": mode_id})
    
    def insert_mode(self, mode: dict[str, Any]) -> str:
        result = self.db.modes.insert_one(mode)
        return str(result.inserted_id)

    def delete_mode_by_id(self, mode_id: ObjectId) -> bool:
        result = self.db.modes.delete_one({"_id": mode_id})
        return bool(result.deleted_count)
