# Flags-App-Game

## Getting Started

### For REACT JS

1. Clone the repository
2. Join to the correct path of the clone
3. Install node_modules with npm install
4. Use npm start to run the app page

### For Flask

1. Join to the correct path of the clone
2. Run the server with python app.py

### For MongoDB

1. Start one window of CMD and run the command `mongod`
2. Start another one window of CMD and run the command `mongo`

## Description

I made a web application with React JS and Flask for the api-rest, I used mongodb to save the information. In this web application you can play guess the flag, there are a total of 3 game modes among them we have normal, hard and hardcore mode. In each of them will appear 5 flags and depending on the game mode will have more or less time. In game modes with a higher difficulty the points multiplier will be higher, because every time you guess a flag you add points. In each game mode there is a ranking and there is also a global ranking of players that is governed by the amount of points they score.

## Technologies used

1. REACT JS
2. FLASK
3. CSS
4. MONGO DB

## Libraries used

1. Pymongo

## Galery

![flags-App-Page](https://raw.githubusercontent.com/DiegoLibonati/DiegoLibonatiWeb/main/data/projects/Flask/Imagenes/flagsgame-0.jpg)

![flags-App-Page](https://raw.githubusercontent.com/DiegoLibonati/DiegoLibonatiWeb/main/data/projects/Flask/Imagenes/flagsgame-1.jpg)

![flags-App-Page](https://raw.githubusercontent.com/DiegoLibonati/DiegoLibonatiWeb/main/data/projects/Flask/Imagenes/flagsgame-2.jpg)

![flags-App-Page](https://raw.githubusercontent.com/DiegoLibonati/DiegoLibonatiWeb/main/data/projects/Flask/Imagenes/flagsgame-3.jpg)

![flags-App-Page](https://raw.githubusercontent.com/DiegoLibonati/DiegoLibonatiWeb/main/data/projects/Flask/Imagenes/flagsgame-4.jpg)

## Portfolio Link

`https://diegolibonati.github.io/DiegoLibonatiWeb/#/projects?q=Flags%20Game%20App%20Page`

## Video

https://user-images.githubusercontent.com/99032604/199865818-646e2a21-c6a4-42d6-976d-3b4861c5990c.mp4

## Documentation

### Flask

`add_flag()` is an endpoint that will allow us to add a new flag:

```
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
```

`flags()` is an endpoint that will return all the flags:

```
@app.route('/flags/allflags', methods=["GET"])
@cross_origin()
def flags():

   documents = json_util.dumps(mongo.db.flags.find())

   return Response(documents, mimetype='application/json')
```

`flags_mode()` is an endpoint that will return the game mode we want to access:

```
@app.route('/flags/<mode>', methods=["GET"])
@cross_origin()
def flags_mode(mode):

    mode_to_search = mode.lower()

    if mode_to_search == "normal" or mode_to_search == "hard" or mode_to_search == "hardcore":
        documents = mongo.db.flags.aggregate([ { "$sample": {"size": 5} } ])

        response = json_util.dumps(documents)

        return Response(response, mimetype='application/json')
```

`add_mode()` is an endpoint that will allow us to add a new mode:

```
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
```

`find_mode()` is an endpoint that will allow us to search for a mode:

```
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
```

`add_or_modify()` is an endpoint that will allow us to add or edit a player:

```
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
```

`top_general()` is an endpoint that will allow us to obtain the general top:

```
@app.route('/users/top/general', methods=['GET'])
@cross_origin()
def top_general():

    top_ten_general = mongo.db.users.find({},{ "_id":0 ,"username": 1, "modes.general_score":1}).sort([("modes.0.general_score", -1)]).limit(10)

    response = json_util.dumps(top_ten_general)

    return Response(response , mimetype='application/json')
```

`top_mode()` is an endpoint that will allow us to obtain the top of a particular mode, which we want to access:

```
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
```

`not_accepted()` is an endpoint that allows us to have a route in case there is an error:

```
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
```

### React JS

### Folder: pages

In the `pages` folder we will find all the pages that our application has, among them we can find `FinishGameOPage, HomePage, MenuModePage, MenuPage,ModePage`.

### hooks: CustomHooks

`useCountdown.js` is a CustomHook that works like a counter, this CustomHook in this application is used when the player is playing and has a time to finish playing before he runs out of time.
`useFetch.js` is a CustomHook that is used to obtain information and dump it to our states in order to render that information that comes to us from the API.
`useForm.js` is a CustomHook that allows us to handle all of our application forms.
`useLogic.js` is a CustomHook that handles all the logic once the game starts, since the user guesses or not the name of a flag, the score that will be awarded according to the time that goes by, the colors of the input by if it fails or hits etc.
`useRequest.js` is a CustomHook that is responsible for making the `request` to the endpoints of our Flask server to obtain the information we want.

### helpers

`getFinishGame()` is a function that will let us know when the game is over:

```
export const getFinishGame = (timeleft, index, array, setFinishGame) => {
  const timeleftSplit = timeleft.split(":");

  const mins = timeleftSplit[1];
  const secs = timeleftSplit[2];

  if (
    (mins === "00" && secs === "00") ||
    (array.length - 1 < index && index && array)
  ) {
    setFinishGame(true);
  }
};
```

`getTop()` is a function that will allow us to get the top in a specific way:

```
export const getTop = (modes, modeName) => {
  let finalScore = 0;

  modes.forEach(function (mode) {
    if (mode[modeName]) {
      finalScore = mode[modeName];
    }
  });

  return finalScore;
};
```

### Context: FlagsContext.jsx

The `navbar` state will allow us to manage the navbar in its mobile version, `btnStart` is a state that will allow us to know when the button was touched, `score` will be the state where the user's score is saved, ` flagsUrl` is a state that will allow us to designate a specific URL to make a request, `modeURL` works the same way but for endpoints in relation to the mode and `topUrl` works the same way as the other two but this one for top request urls:

```
const [navbar, setNavbar] = useState(false);
const [btnStart, setBtnStart] = useState(false);
const [score, setScore] = useState(0);
const [flagsUrl, setFlagsUrl] = useState([]);
const [modeUrl, setModeUrl] = useState([]);
const [topUrl, setTopUrl] = useState([]);
```
