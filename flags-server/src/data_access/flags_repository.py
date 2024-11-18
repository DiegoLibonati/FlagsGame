from typing import Any
from bson import ObjectId

from flask_pymongo.wrappers import Database


class FlagRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def get_all_flags(self) -> list[dict[str, Any]]:
        return list(self.db.flags.find())
    
    def get_flag(self, flag_id: ObjectId) -> dict[str, Any]:
        return self.db.flags.find_one({"_id": flag_id})

    def insert_flag(self, flag: dict[str, Any]) -> str:
        result = self.db.flags.insert_one(flag)
        return str(result.inserted_id)

    def get_random_flags(self, quantity: int) -> list[dict[str, Any]]:
        return list(self.db.flags.aggregate([{"$sample": {"size": quantity}}]))

    def delete_flag_by_id(self, flag_id: ObjectId) -> bool:
        result = self.db.flags.delete_one({"_id": flag_id})
        return bool(result.deleted_count)
