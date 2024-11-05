from typing import Any
from bson import ObjectId

from flask import current_app

def parse_flags(flags: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [{**flag, "_id": str(flag["_id"])} for flag in flags]


def parse_modes(modes: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [{**mode, "_id": str(mode["_id"])} for mode in modes]


def parse_mode(mode: dict[str, Any]) -> dict[str, str]:
    return {key: str(value) if isinstance(value, ObjectId) else str(value) for key, value in mode.items()}


def get_list_modes(modes: list[dict[str, Any]]) -> list[str]:
    return [mode.get('name').lower() for mode in modes]


def get_list_users_by_sorted_score(users: list[dict[str, Any]], mode_name_score: str) -> list[dict[str, Any]]:
    data = []
    
    for user in users:
        user_in_top = {}
        
        user_modes = user.get("modes")
        for user_mode in user_modes:
            if user_mode.get(mode_name_score) or user_mode.get(mode_name_score) == 0:
                user_in_top["score"] = user_mode[mode_name_score]
                    
        user_in_top["_id"] = str(user.get("_id"))
        user_in_top["username"] = user.get("username")

        data.append(user_in_top)

    if not data:
        return []

    current_app.logger.error(data)

    data.sort(key=lambda x: x['score'], reverse=True)

    return data