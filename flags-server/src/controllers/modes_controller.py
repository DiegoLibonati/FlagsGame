from flask import make_response, current_app, request
from bson import json_util


def find_mode(name : str) -> tuple:
    name = name.capitalize()

    mode = current_app.mongo.db.modes.find_one({"name": name})

    if mode == None:
        name = name.lower()
        mode = current_app.mongo.db.modes.find_one({"name": name})

    response = json_util.dumps(mode)

    return make_response(
        response,
    200)


def add_mode() -> tuple:
    name = request.json['name']
    description = request.json['description']
    timeleft = request.json['timeleft']

    name = name.strip()
    description = description.strip()

    if (name and description and timeleft) and (not name.isspace() and not description.isspace()):
        current_app.mongo.db.modes.insert_one({
            'name': name,
            'description':description,
            'timeleft':timeleft,
        })

    response = {
        'name': name,
        'description':description,
        'timeleft':timeleft,
    }

    return make_response(
        response,
    201)


def top_mode(mode: str) -> tuple:
    index = None
    modes = current_app.mongo.db.modes.find({}, {"_id":0, "name":1})
    
    for idx, item in enumerate(modes):
        if item["name"].lower() == mode:
            index = idx + 1
    
    top_ten_mode = current_app.mongo.db.users.find({},{ "_id":0 ,"username": 1, f"modes.{mode}":1}).sort([(f"modes.{index}.{mode}", -1)]).limit(10)

    response = json_util.dumps(top_ten_mode)

    return make_response(
        response,
    200)