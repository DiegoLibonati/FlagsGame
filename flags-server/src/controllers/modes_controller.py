from typing import Any

from flask import make_response
from flask import current_app 
from flask import request

from src.utils.utils import parse_mode
from src.utils.utils import parse_modes
from src.utils.utils import get_list_modes_names
from src.utils.utils import get_list_users_by_sorted_score


def get_modes() -> dict[str, Any]:
    modes = current_app.mongo.db.modes.find()
    data = parse_modes(modes)

    return make_response({
        "message": "Successfully obtained modes.",
        "data": data
    }, 200)


def find_mode(name : str) -> dict[str, Any]:
    if not name:
        return make_response({
            "message": "A game mode with this name was not found, please enter valid fields.",
            "fields": {
                "name": name
            },
            "data": None
        }, 400)

    mode = current_app.mongo.db.modes.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})

    if not mode:
        return make_response({
            "message": "A game mode with this name was not found, please enter valid fields.",
            "fields": {
                "name": name
            },
            "data": None
        }, 400)

    data = parse_mode(mode)

    return make_response({
        "message": "Successfully obtained the requested mode.",
        "data": data
    }, 200)


def add_mode() -> dict[str, Any]:
    name = request.json['name']
    description = request.json['description']
    timeleft = request.json['timeleft']
    multiplier = request.json['multiplier']

    name = name.strip()
    description = description.strip()

    mode = {
        'name': name,
        'description': description,
        'timeleft': timeleft,
        'multiplier': multiplier,
    }

    if not name or not description or not timeleft or not multiplier:
        return make_response({
            "message": f"The mode could not be added because the fields entered are not valid.",
            "fields": mode
        }, 400)

    result_insert = current_app.mongo.db.modes.insert_one(mode)
    mode['_id'] = str(result_insert.inserted_id)

    return make_response({
        "message": f"Successfully created new mode",
        "fields": mode
    }, 201)


def top_mode(mode: str) -> dict[str, Any]:
    data = []
    mode_name = mode.lower()
    modes = current_app.mongo.db.modes.find({} , { "_id":0 ,"name": 1})
    modes = get_list_modes_names(modes=modes)
    users = current_app.mongo.db.users.find()

    if not modes or not mode_name in modes or not users:
        return make_response({ 
            "message": "The top could not be obtained as requested.",
            "fields": {
                "mode": mode,
            },
            "data": []
        }, 400)

    data = get_list_users_by_sorted_score(users=users, mode_name_score=mode_name)
    data = data[:10]

    return make_response({
        "message": "The top ten of the requested mode was obtained.",
        "data": data
    }, 200)