from typing import Any
from bson import ObjectId

from flask_pymongo.wrappers import Database


class UserRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def get_all_users(self) -> list[dict[str, Any]]:
        return list(self.db.users.find())

    def get_user_by_username(self, username: str) -> dict[str, Any]:
        return self.db.users.find_one({"username": username})
    
    def get_user_by_id(self, user_id: ObjectId) -> dict[str, Any]:
        return self.db.users.find_one({"_id": user_id})

    def insert_user(self, user: dict[str, Any]) -> str:
        result = self.db.users.insert_one(user)
        return str(result.inserted_id)
    
    def update_user_by_username(self, username: str, values: dict[str, Any]) -> str:
        return self.db.users.update_one({'username': username}, {'$set': values})
    
    def delete_user_by_id(self, user_id: ObjectId) -> bool:
        result = self.db.users.delete_one({"_id": user_id})
        return bool(result.deleted_count)
