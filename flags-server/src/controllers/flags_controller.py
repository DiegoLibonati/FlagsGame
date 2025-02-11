from bson import ObjectId

from flask import make_response
from flask import current_app
from flask import request
from flask import Response

from src.models.Flag import Flag
from src.models.FlagManager import FlagManager


def flags() -> Response:
    flag_manager = FlagManager()
    flags = current_app.flag_repository.get_all_flags()

    if flags: flag_manager.add_flags(flags=flags)

    data = flag_manager.parse_items()

    return make_response({
        "message": "The flags were successfully obtained.",
        "data": data
    }, 200)


def add_flag() -> Response:
    image = request.json.get('image', "").strip()
    name = request.json.get('name', "").strip()
    
    if not name or not image:
        return make_response({
            "message": f"The flag could not be added because the fields are not valid.",
            "data": None
        }, 400)
    
    inserted_id = current_app.flag_repository.insert_flag(flag={"name": name, "image": image})
    
    flag = Flag(
        _id=ObjectId(inserted_id),
        name=name,
        image=image
    )

    return make_response({
        "message": "New flag added.",
        "data": flag.to_dict()
    }, 201)


def get_random_flags(quantity: str) -> Response:
    try:
        quantity = int(quantity)

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
    except ValueError:
            return make_response({
                "message": "Invalid quantity. It must be a positive integer.",
                "data": []
            }, 400)

    flag_manager = FlagManager()
    flags = current_app.flag_repository.get_random_flags(quantity=quantity)

    if flags: flag_manager.add_flags(flags=flags)      

    data = flag_manager.parse_items()

    return make_response({
        "message": "The flags were obtained randomly.",
        "data": data
    }, 200)


def delete_flag(id: str) -> Response:
    try:
        object_id = ObjectId(id)
        document = current_app.flag_repository.get_flag(flag_id=object_id)

        if not document: 
            return make_response({
                "message": f"No flag found with id: {id}.",
                "data": None
            }, 404)
        
        flag = Flag(**document)

        current_app.flag_repository.delete_flag_by_id(flag_id=flag.id)

        return make_response({
            "message": f"Flag with id: {id} was deleted.",
            "data": flag.to_dict()
        }, 200)
    except Exception as e: 
        return make_response({
            "message": f"Error deleting flag: {str(e)}"
        }, 400)