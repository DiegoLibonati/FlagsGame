from flask import Flask, request, Response, jsonify
from bson import json_util
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost/flags"
app.config['JSON_AS_ASCII'] = False
mongo = PyMongo(app)
CORS(app)

@app.route('/flags/newflag', methods=['POST'])
def add_flag():

    image = request.json['image']
    name = request.json['name']

    image = image.strip()
    name = name.strip()

    if (image and name) and (not image.isspace() and not name.isspace()):
        mongo.db.flags.insert_one({
            'image':image,
            'name':name,
        })

    response = {
        'image':image,
        'name':name,
    }

    return f"{response}"

@app.route('/flags/allflags', methods=["GET"])
@cross_origin()
def flags():

   documents = json_util.dumps(mongo.db.flags.find())

   return Response(documents, mimetype='application/json')

@app.route('/flags/<mode>', methods=["GET"])
@cross_origin()
def flags_mode(mode):

    mode_to_search = mode.lower()

    if mode_to_search == "normal" or mode_to_search == "hard" or mode_to_search == "hardcore":
        documents = mongo.db.flags.aggregate([ { "$sample": {"size": 5} } ])

        response = json_util.dumps(documents)

        return Response(response, mimetype='application/json')

@app.route('/modes/newmode', methods=['POST'])
@cross_origin()
def add_mode():

    name = request.json['name']
    description = request.json['description']
    timeleft = request.json['timeleft']

    name = name.strip()
    description = description.strip()
    


    if (name and description and timeleft) and (not name.isspace() and not description.isspace()):
        mongo.db.modes.insert_one({
            'name': name,
            'description':description,
            'timeleft':timeleft,
        })

    response = {
            'name': name,
            'description':description,
            'timeleft':timeleft,
        }

    return Response(response, mimetype='application/json')

@app.route('/modes/findmode/<name>', methods=['GET'])
@cross_origin()
def find_mode(name):

    name = name.capitalize()

    mode = mongo.db.modes.find_one({"name": name})

    if mode == None:
        name = name.lower()
        mode = mongo.db.modes.find_one({"name": name})

    response = json_util.dumps(mode)
    return Response(response, mimetype='application/json')

@app.route('/users/addormodify', methods=['POST', 'PUT'])
@cross_origin()
def add_or_modify():

    modes_keys = []

    username = request.json['username'].strip()
    password = request.json['password'].strip()
    score_actual = request.json['score']
    mode_name = request.json['mode_name'].strip().lower()

    username_db = mongo.db.users.find_one({"username": username})
    modes_db = mongo.db.modes.find()

    try:
        user_db_password = username_db["password"]
        user_db_modes_played = username_db["modes"]

        for mode in user_db_modes_played:
            for key, value in mode.items():
                modes_keys.append(key)
    except:
        pass

    if not username_db and request.method == "POST":

        modes = [{"general_score": score_actual}]

        for mode in modes_db:
            for key, value in mode.items():
                if key == "name":
                    value = str(value).lower()
                    if value == mode_name:
                        modes.append({str(value).lower(): score_actual})
                    else:
                        modes.append({str(value).lower(): 0})

        if username and password and (not username.isspace() and not password.isspace()):
            mongo.db.users.insert_one({
            'username': username,
            'password': generate_password_hash(password),
            'modes': modes
            })

            response = json_util.dumps({"message":"User successfully added"},)

            return Response(response, mimetype='application/json')

        else:
            
            return not_accepted("Username or password invalid", 406)

    elif username_db and request.method == "POST":

        return not_accepted("There is a user with that username", 406)


    elif username_db and request.method == "PUT" and mode_name in modes_keys:

        if check_password_hash(user_db_password, password):

            for index, mode_played in enumerate(user_db_modes_played):
                for mode, score in mode_played.items():
                    if mode == mode_name:
                        new_general_score = (username_db["modes"][0]["general_score"] - username_db["modes"][index][mode_name]) + score_actual
                        mongo.db.users.update_one({"username": username}, {"$set" : {f"modes.{index}.{mode}":score_actual, f"modes.0.general_score":new_general_score}})

                        response = json_util.dumps({"message":"User successfully updated"},)

            return Response(response)
        else:
            return not_accepted("Password do not match with that username", 406)

    elif username_db and request.method == "PUT" and not mode_name in modes_keys:
        
        new_general_score = score_actual + username_db["modes"][0]["general_score"]

        if check_password_hash(user_db_password, password):

            mongo.db.users.update_one({"username": username}, {"$push": {"modes":{mode_name: score_actual}, "$set": {"modes.0.general_score": new_general_score}}})

        response = json_util.dumps({"message":"Successfully added mode"},)

        return Response(response)

    elif not username_db and request.method == "PUT":
        return not_accepted("There is not a user with that username created", 406)

@app.route('/users/top/general', methods=['GET'])
@cross_origin()
def top_general():

    top_ten_general = mongo.db.users.find({},{ "_id":0 ,"username": 1, "modes.general_score":1}).sort([("modes.0.general_score", -1)]).limit(10)
    
    response = json_util.dumps(top_ten_general)

    return Response(response , mimetype='application/json')

@app.route('/mode/top/<mode>', methods=['GET'])
@cross_origin()
def top_mode(mode):

    index = None
    modes = mongo.db.modes.find({}, {"_id":0, "name":1})
    
    for idx, item in enumerate(modes):
        if item["name"].lower() == mode:
            index = idx + 1
    
    top_ten_mode = mongo.db.users.find({},{ "_id":0 ,"username": 1, f"modes.{mode}":1}).sort([(f"modes.{index}.{mode}", -1)]).limit(10)

    response = json_util.dumps(top_ten_mode)

    return Response(response, mimetype='application/json')

@app.errorhandler(406)
@cross_origin()
def not_accepted(message=None, status = 406):

    response = jsonify({
        'message': message,
        'status': status
    })

    response.status_code = 406

    return response

if __name__ == "__main__":
    app.run(debug=True)
    