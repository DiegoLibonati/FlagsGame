# FlagsGame

## Educational Purpose

This project was created primarily for **educational and learning purposes**.  
While it is well-structured and could technically be used in production, it is **not intended for commercialization**.  
The main goal is to explore and demonstrate best practices, patterns, and technologies in software development.

## Getting Started

1. Clone the repository with `git clone "repository link"`
2. Join to `flags-game-app` folder and execute: `npm install` or `yarn install` in the terminal
3. Go to the previous folder and execute: `docker-compose -f dev.docker-compose.yml build --no-cache` in the terminal
4. Once built, you must execute the command: `docker-compose -f dev.docker-compose.yml up --force-recreate` in the terminal

NOTE: You have to be standing in the folder containing the: `dev.docker-compose.yml` and you need to install `Docker Desktop` if you are in Windows.

### Pre-Commit for Development (Python)

NOTE: Install **pre-commit** inside: `bookstore-server` folder.

1. Once you're inside the virtual environment, let's install the hooks specified in the pre-commit. Execute: `pre-commit install`
2. Now every time you try to commit, the pre-commit lint will run. If you want to do it manually, you can run the command: `pre-commit run --all-files`

## Description

I made a web application with React JS and Flask for the api-rest, I used mongodb to save the information. In this web application you can play guess the flag, there are a total of 3 game modes among them we have normal, hard and hardcore mode. In each of them will appear 5 flags and depending on the game mode will have more or less time. In game modes with a higher difficulty the points multiplier will be higher, because every time you guess a flag you add points. In each game mode there is a ranking and there is also a global ranking of players that is governed by the amount of points they score.

## Technologies used

1. React
2. Typescript
3. CSS3
4. HTML5
5. Vite

BackEnd:

1. Python -> Flask

Deploy:

1. Docker
2. Nginx
3. Gunicorn

Database:

1. MongoDB -> PyMongo

## Libraries used

### Frontend

#### Dependencies

```
"react": "^18.2.0",
"react-dom": "^18.2.0",
"react-icons": "^4.4.0",
"react-router-dom": "^6.3.0",
"web-vitals": "^2.1.4"
```

#### devDependencies

```
"@testing-library/dom": "^10.4.0"
"@testing-library/jest-dom": "^6.6.2"
"@testing-library/react": "^16.0.1"
"@testing-library/user-event": "^14.5.2"
"@types/jest": "^29.5.13"
"@types/node": "^20.10.6"
"@types/react": "^18.3.11"
"@types/react-dom": "^18.3.1"
"@vitejs/plugin-react": "^5.0.2"
"jest": "^29.7.0"
"jest-environment-jsdom": "^29.7.0"
"jest-fixed-jsdom": "^0.0.9"
"msw": "^2.6.0"
"ts-jest": "^29.2.5"
"ts-node": "^10.9.2"
"typescript": "^4.9.5"
"vite": "^7.1.7"
```

### Backend

#### Requirements.txt

```
Flask==3.1.2
Flask-PyMongo==3.0.1
pydantic==2.11.9
werkzeug==3.1.3
gunicorn==23.0.0
pre-commit==4.3.0
```

#### Requirements.test.txt

```
pytest==8.4.2
pytest-env==1.1.5
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/FlagsGame`](https://www.diegolibonati.com.ar/#/project/FlagsGame)

## Video

https://user-images.githubusercontent.com/99032604/199865818-646e2a21-c6a4-42d6-976d-3b4861c5990c.mp4

## Testing

### Frontend

1. Join to `flags-game-app` folder
2. Execute: `yarn test` or `npm test`

### Backend

1. Join to the correct path of the clone and join to: `flags-server`
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute: `pip install -r requirements.txt`
5. Execute: `pip install -r requirements.test.txt`
6. Execute: `pytest --log-cli-level=INFO`

### **Version**

```ts
APP VERSION: 0.0.1
README UPDATED: 28/09/2025
AUTHOR: Diego Libonati
```

### **Env Keys**

1. `TZ`: Refers to the timezone setting for the container.
2. `VITE_API_URL`: Refers to the base URL of the backend API the frontend consumes.
3. `MONGO_URI`: Refers to the connection URI for the MongoDB database, including user, password, host, port, database name, and auth source.
4. `HOST`: Refers to the network interface where the backend API listens (e.g., 0.0.0.0 to allow external connections).
5. `PORT`: Refers to the port on which the backend API is exposed.
6. `DEBUG_MODE`: Refers to enabling or disabling debug mode for backend lo

```ts
# Frontend Envs
TZ=America/Argentina/Buenos_Aires

VITE_API_URL=http://host.docker.internal:5050

# Backend Envs
TZ=America/Argentina/Buenos_Aires

MONGO_URI=mongodb://admin:secret123@bookstore-db:27017/bookstore?authSource=admin

HOST=0.0.0.0
PORT=5050
DEBUG_MODE=true
```

### **Flags Endpoints API**

---

- **Endpoint Name**: Get Flags
- **Endpoint Method**: GET
- **Endpoint Prefix**: /api/v1/flags/
- **Endpoint Fn**: This endpoint obtains all the flags
- **Endpoint Params**: None

---

- **Endpoint Name**: Get Random Flags
- **Endpoint Method**: GET
- **Endpoint Prefix**: /api/v1/flags/random/:quantity
- **Endpoint Fn**: This endpoint obtains random flags by quantity
- **Endpoint Params**: 

```ts
{
  quantity: number;
}
```

---

- **Endpoint Name**: Create Flag
- **Endpoint Method**: POST
- **Endpoint Prefix**: /api/v1/flags/
- **Endpoint Fn**: This endpoint create a new Flag
- **Endpoint Body**:

```ts
{
    name: string;
    image: string;
}
```

---

- **Endpoint Name**: Delete Flag
- **Endpoint Method**: DELETE
- **Endpoint Prefix**: /api/v1/flags/:id
- **Endpoint Fn**: This endpoint deletes a Flag by id
- **Endpoint Params**: 

```ts
{
  id: string;
}
```

---

- **Endpoint Name**: Get Modes
- **Endpoint Method**: GET
- **Endpoint Prefix**: /api/v1/modes/
- **Endpoint Fn**: This endpoint obtains all the modes
- **Endpoint Params**: None

---

- **Endpoint Name**: Get Mode
- **Endpoint Method**: GET
- **Endpoint Prefix**: /api/v1/modes/:idMode
- **Endpoint Fn**: This endpoint obtains a mode by id
- **Endpoint Params**: 

```ts
{
  quantity: idMode;
}
```

---

- **Endpoint Name**: Create Mode
- **Endpoint Method**: POST
- **Endpoint Prefix**: /api/v1/modes/
- **Endpoint Fn**: This endpoint create a new Mode
- **Endpoint Body**:

```ts
{
    name: string;
    description: string;
    timeleft: number;
    multiplier: number;
}
```

---

- **Endpoint Name**: Get Top Ten Mode
- **Endpoint Method**: GET
- **Endpoint Prefix**: /api/v1/modes/:idMode
- **Endpoint Fn**: This endpoint obtains the top ten of the mode by id
- **Endpoint Params**: 

```ts
{
  id: string;
}
```

---

- **Endpoint Name**: Delete Mode
- **Endpoint Method**: DELETE
- **Endpoint Prefix**: /api/v1/modes/:id
- **Endpoint Fn**: This endpoint deletes a Mode by id
- **Endpoint Params**: 

```ts
{
  id: string;
}
```

---

- **Endpoint Name**: Create User
- **Endpoint Method**: POST
- **Endpoint Prefix**: /api/v1/users/
- **Endpoint Fn**: This endpoint create a new User
- **Endpoint Body**:

```ts
{
    username: string;
    password: string;
    score: number;
    mode_id: string;
}
```

---

- **Endpoint Name**: Update User
- **Endpoint Method**: PATCH
- **Endpoint Prefix**: /api/v1/users/
- **Endpoint Fn**: This endpoint update a new User
- **Endpoint Body**:

```ts
{
    username: string;
    password: string;
    score: number;
    mode_id: string;
}
```

---

- **Endpoint Name**: Get Top Ten Global
- **Endpoint Method**: GET
- **Endpoint Prefix**: /api/v1/users/top_global
- **Endpoint Fn**: This endpoint obtains the top general
- **Endpoint Params**: None

---

- **Endpoint Name**: Delete User
- **Endpoint Method**: DELETE
- **Endpoint Prefix**: /api/v1/users/:id
- **Endpoint Fn**: This endpoint deletes a User by id
- **Endpoint Params**: 

```ts
{
  id: string;
}
```

---

## Known Issues