# Flags-App-Game

## Getting Started

1. Clone the repository with `git clone "repository link"`
2. Go to the folder where you cloned your repository
3. Run `docker-compose build --no-cache` in the terminal
4. Once built, you must execute the command: `docker-compose up`
5. You have to be standing in the folder containing the: `docker-compose.yml`

## Description

I made a web application with React JS and Flask for the api-rest, I used mongodb to save the information. In this web application you can play guess the flag, there are a total of 3 game modes among them we have normal, hard and hardcore mode. In each of them will appear 5 flags and depending on the game mode will have more or less time. In game modes with a higher difficulty the points multiplier will be higher, because every time you guess a flag you add points. In each game mode there is a ranking and there is also a global ranking of players that is governed by the amount of points they score.

## Technologies used

1. REACT JS
2. FLASK
3. PYTHON
4. TYPESCRIPT
5. CSS3
6. MONGO DB

## Libraries used

1. Pymongo

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/11`](https://www.diegolibonati.com.ar/#/project/11)

## Video

https://user-images.githubusercontent.com/99032604/199865818-646e2a21-c6a4-42d6-976d-3b4861c5990c.mp4

## Documentation

### Flask

`add_flag()` is an endpoint that will allow us to add a new flag:

```
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
```

`flags()` is an endpoint that will return all the flags:

```
def flags() -> tuple:
    documents = json_util.dumps(current_app.mongo.db.flags.find())

    return make_response(
        documents, 
    200)
```

`flags_mode()` is an endpoint that will return the game mode we want to access:

```
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
```

`add_mode()` is an endpoint that will allow us to add a new mode:

```
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
```

`find_mode()` is an endpoint that will allow us to search for a mode:

```
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
```

`add_or_modify()` is an endpoint that will allow us to add or edit a player:

```
def add_or_modify() -> tuple:
    modes_keys = []

    username = request.json['username'].strip()
    password = request.json['password'].strip()
    score_actual = request.json['score']
    mode_name = request.json['mode_name'].strip().lower()

    username_db = current_app.mongo.db.users.find_one({"username": username})
    modes_db = current_app.mongo.db.modes.find()

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
            current_app.mongo.db.users.insert_one({
                'username': username,
                'password': generate_password_hash(password),
                'modes': modes
            })

            response = json_util.dumps({"message":"User successfully added"},)

            return make_response(
                response, 
            201)

        else:
            
            return not_accepted("Username or password invalid", 406)

    elif username_db and request.method == "POST":

        return not_accepted("There is a user with that username", 406)


    elif username_db and request.method == "PUT" and mode_name in modes_keys:

        if check_password_hash(user_db_password, password):

            for index, mode_played in enumerate(user_db_modes_played):
                for mode, _ in mode_played.items():
                    if mode == mode_name:
                        new_general_score = (username_db["modes"][0]["general_score"] - username_db["modes"][index][mode_name]) + score_actual
                        current_app.mongo.db.users.update_one({"username": username}, {"$set" : {f"modes.{index}.{mode}":score_actual, f"modes.0.general_score":new_general_score}})

                        response = json_util.dumps({"message":"User successfully updated"},)

            return make_response(
                response, 
            201)
        else:
            return not_accepted("Password do not match with that username", 406)

    elif username_db and request.method == "PUT" and not mode_name in modes_keys:
        
        new_general_score = score_actual + username_db["modes"][0]["general_score"]

        if check_password_hash(user_db_password, password):

            current_app.mongo.db.users.update_one({"username": username}, {"$push": {"modes":{mode_name: score_actual}, "$set": {"modes.0.general_score": new_general_score}}})

        response = json_util.dumps({"message":"Successfully added mode"},)

        return make_response(
            response, 
        201)

    elif not username_db and request.method == "PUT":
        return not_accepted("There is not a user with that username created", 406)
```

`top_general()` is an endpoint that will allow us to obtain the general top:

```
def top_general() -> tuple:
    top_ten_general = current_app.mongo.db.users.find({},{ "_id":0 ,"username": 1, "modes.general_score":1}).sort([("modes.0.general_score", -1)]).limit(10)
    
    response = json_util.dumps(top_ten_general)

    return make_response(
        response,
    200)
```

`top_mode()` is an endpoint that will allow us to obtain the top of a particular mode, which we want to access:

```
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
```

`not_accepted()` is an endpoint that allows us to have a route in case there is an error:

```
def not_accepted(message: str = "", status: int = 406) -> tuple:

    response = {
        'message': message,
        'status': status
    }

    response.status_code = 406

    return make_response(
        response,
    406)
```

### React JS

### Folder: pages

In the `pages` folder we will find all the pages that our application has, among them we can find `FinishGameOPage, HomePage, MenuModePage, MenuPage,ModePage`.

### hooks: CustomHooks

`useCountdown.tsx` is a CustomHook that works like a counter, this CustomHook in this application is used when the player is playing and has a time to finish playing before he runs out of time.
`useForm.tsx` is a CustomHook that allows us to handle all of our application forms.
`useLogic.tsx` is a CustomHook that handles all the logic once the game starts, since the user guesses or not the name of a flag, the score that will be awarded according to the time that goes by, the colors of the input by if it fails or hits etc.

### helpers

`getFinishGame()` is a function that will let us know when the game is over:

```
export const getFinishGame = (
  timeleft: string,
  index: number,
  array: Flag[],
  setFinishGame: React.Dispatch<React.SetStateAction<boolean>>
): void => {
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
import { Mode } from "../entities/entities";

export const getTop = (modes: Mode[], modeName: string): number => {
  let finalScore = 0;

  modes.forEach(function (mode) {
    if (mode[modeName as keyof typeof mode]) {
      finalScore = Number(mode[modeName as keyof typeof mode]);
    }
  });

  return finalScore;
};
```

### Context: FlagsContext.tsx

```
const [navbar, setNavbar] = useState<boolean>(false);
const [btnStart, setBtnStart] = useState<boolean>(false);
const [score, setScore] = useState<number>(0);

const [flagsArr, setFlagsArr] = useState<Flag[]>([]);
const [flagsLoading, setFlagsLoading] = useState<boolean>(false);

const [actualMode, setActualMode] = useState<Mode | null>(null);
const [modeLoading, setModeLoading] = useState<boolean>(false);

const [topArr, setTopArr] = useState<User[]>([]);
const [topLoading, setTopLoading] = useState<boolean>(false);
```
