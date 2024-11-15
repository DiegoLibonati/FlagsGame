# FlagsGame

## Getting Started

1. Clone the repository with `git clone "repository link"`
2. Go to the folder where you cloned your repository
3. Run `docker-compose build --no-cache` in the terminal
4. Once built, you must execute the command: `docker-compose up --force-recreate`

NOTE: You have to be standing in the folder containing the: `docker-compose.yml`

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

### Frontend

#### Dependencies

```
"@types/jest": "^29.5.13",
"@types/react": "^18.3.11",
"@types/react-dom": "^18.3.1",
"react": "^18.2.0",
"react-dom": "^18.2.0",
"react-icons": "^4.4.0",
"react-scripts": "5.0.1",
"web-vitals": "^2.1.4",
"react-router-dom": "^6.3.0"
```

#### devDependencies

```
"@testing-library/jest-dom": "^6.6.2",
"@testing-library/react": "^16.0.1",
"@testing-library/user-event": "^14.5.2",
"@testing-library/dom": "^10.4.0",
"msw": "^2.6.0",
"typescript": "^5.3.3"
```

### Backend

#### Requirements.txt

```
flask
flask_pymongo
werkzeug
```

#### Requirements.test.txt

```
pytest
pytest-env
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/FlagsGame`](https://www.diegolibonati.com.ar/#/project/FlagsGame)

## Video

https://user-images.githubusercontent.com/99032604/199865818-646e2a21-c6a4-42d6-976d-3b4861c5990c.mp4

## Testing

### Frontend

1. Join to the correct path of the clone and join to: `flags-game-app`
2. Execute: `yarn install`
3. Execute: `yarn test`

### Backend

1. Join to the correct path of the clone and join to: `flags-server`
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute: `pip install -r requirements.txt`
5. Execute: `pip install -r requirements.test.txt`
6. Execute: `pytest --log-cli-level=INFO`