from typing import Any
from bson import ObjectId

from flask import make_response
from flask import current_app 
from flask import request

from utils.utils import parse_flags
from utils.utils import get_list_modes_names


def flags() -> dict[str, Any]:
    documents = current_app.mongo.db.flags.find()
    data = parse_flags(documents)

    return make_response({
        "message": "The flags were successfully obtained.",
        "data": data
    }, 200)


def add_flag() -> dict[str, Any]:
    image = request.json.get('image', "")
    name = request.json.get('name', "")

    image = image.strip()
    name = name.strip()

    flag = {
        'image': image,
        'name': name,
    }

    if not image or not name:
        return make_response({
            "message": f"The flag could not be added because the fields are not valid.",
            "fields": flag
        }, 400)

    result_insert = current_app.mongo.db.flags.insert_one(flag)
    flag['_id'] = str(result_insert.inserted_id)

    return make_response({
        "message": "New flag added.",
        "fields": flag
    }, 201)


def get_random_flags(mode: str) -> dict[str, Any]:
    mode_to_search = mode.lower()

    modes = current_app.mongo.db.modes.find({} , { "_id":0 ,"name": 1})
    modes = get_list_modes_names(modes=modes)

    if not mode_to_search or not modes or not mode_to_search in modes:
        return make_response({
            "message": "The flags could not be obtained randomly.",
            "data": []
        }, 400)

    documents = current_app.mongo.db.flags.aggregate([ { "$sample": {"size": 5} } ])

    data = parse_flags(documents)

    return make_response({
        "message": "The flags were obtained randomly.",
        "data": data
    }, 200)


def delete_flag(id: str) -> dict[str, Any]:
    try:
        current_app.mongo.db.flags.delete_one({
            "_id": ObjectId(id)
        })

        return make_response({
            "message": f"{id} was deleted."
        }, 200)
    except Exception as e:
        return make_response({
            "message": str(e)
        }, 400)