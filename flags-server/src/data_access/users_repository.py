from typing import Any

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
    def insert_user(user: User) -> str:
        result = current_app.mongo.db.users.insert_one({'username': user.username, 'password': user.password_hashed, 'scores': user.scores, 'total_score': user.total_score})
        return str(result.inserted_id)
    
    @staticmethod
    def update_user_by_username(username: str, values: dict[str, Any]) -> str:
        return current_app.mongo.db.users.update_one({'username': username}, {'$set': values})