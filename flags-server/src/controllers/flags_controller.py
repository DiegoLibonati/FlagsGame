from flask import make_response, current_app,  request
from bson import json_util


def flags() -> tuple:
    documents = json_util.dumps(current_app.mongo.db.flags.find())

    return make_response(
        documents, 
    200)


def add_flag() -> tuple:
    image = request.json['image']
    name = request.json['name']

    image = image.strip()
    name = name.strip()

    if (image and name) and (not image.isspace() and not name.isspace()):
        current_app.mongo.db.flags.insert_one({
            'image':image,
            'name':name,
        })

    response = {
        'image':image,
        'name':name,
    }

    return make_response(
        f"New flag added: {response}",
    201)


def get_random_flags(mode: str) -> tuple:
    mode_to_search = mode.lower()

    if mode_to_search == "normal" or mode_to_search == "hard" or mode_to_search == "hardcore":
        documents = current_app.mongo.db.flags.aggregate([ { "$sample": {"size": 5} } ])

        response = json_util.dumps(documents)

        return make_response(
            response,
        200)
    
    return make_response(
        [],
    200)