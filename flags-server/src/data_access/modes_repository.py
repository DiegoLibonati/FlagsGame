from typing import Any

from flask import current_app


class ModeRepository:
    @staticmethod
    def get_all_modes() -> list[dict[str, Any]]:
        return list(current_app.mongo.db.modes.find())

    @staticmethod
    def get_mode(name: str) -> dict[str, Any]:
        return current_app.mongo.db.modes.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
    
    @staticmethod
    def insert_mode(mode: dict[str, Any]) -> str:
        result = current_app.mongo.db.modes.insert_one(mode)
        return str(result.inserted_id)

