from typing import Any
from bson import ObjectId

from flask import current_app

from src.models.User import User


class UserRepository:
    @staticmethod
    def get_all_users() -> list[dict[str, Any]]:
        return list(current_app.mongo.db.users.find())

    @staticmethod
    def get_user_by_username(username: str) -> dict[str, Any]:
        return current_app.mongo.db.users.find_one({"username": username})
    
    @staticmethod
    def get_user_by_id(user_id: ObjectId) -> dict[str, Any]:
        return current_app.mongo.db.users.find_one({"_id": user_id})

    @staticmethod
    def insert_user(user: User) -> str:
        result = current_app.mongo.db.users.insert_one({'username': user.username, 'password': user.password_hashed, 'scores': user.scores, 'total_score': user.total_score})
        return str(result.inserted_id)
    
    @staticmethod
    def update_user_by_username(username: str, values: dict[str, Any]) -> str:
        return current_app.mongo.db.users.update_one({'username': username}, {'$set': values})
    
    @staticmethod
    def delete_user_by_id(user_id: ObjectId) -> bool:
        result = current_app.mongo.db.users.delete_one({"_id": user_id})
        return bool(result.deleted_count)
