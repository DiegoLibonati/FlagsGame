# BLUEPRINTS
PREFIX_FLAGS_BP = "/v1/flags"
PREFIX_MODES_BP = "/v1/modes"
PREFIX_USERS_BP = "/v1/users"

# MOCK FLAGS
TEST_FLAG_MOCK = {
    "_id": "673773206d0e53d0d63f3341",
    "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVnagHgbpRUO82-sIOEi3TX1N3wUGSlRWKZQ&s",
    "name": "test_flag"
}
TEST_FLAGS_MOCK = [
    {
        "_id": "67267fd72e10fe5f0af5d706",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVnagHgbpRUO82-sIOEi3TX1N3wUGSlRWKZQ&s",
        "name": "Argentina"
    },
    {
        "_id": "672680152e10fe5f0af5d707",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/1200px-Flag_of_Brazil.svg.png",
        "name": "Brasil"
    },
    {
        "_id": "6726819e0291c4ae90b6798c",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQt5fAr3G2SRs1TaR3jSiGhYPOdxu4mj8sBtg&s",
        "name": "Peru"
    },
    {
        "_id": "672681ac0291c4ae90b6798d",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyiYirHiGCymBqqOjCzm5A71AuealRFxjiUA&s",
        "name": "Canada"
    },
    {
        "_id": "672681bf0291c4ae90b6798e",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-bu9g_Be9LrSEFgXHGT0jX11SCVgzZNaOfA&s",
        "name": "Estados Unidos"
    },
    {
        "_id": "6728cc43d19b644f5bc6e495",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQilbazSxXoEzGPXF0J5Oy3FzGUAgxuMu7upg&s",
        "name": "Colombia"
    },
    {
        "_id": "6738a4c6ca44bc6236c37cc4",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVnagHgbpRUO82-sIOEi3TX1N3wUGSlRWKZQ&s",
        "name": "test_flag"
    }
]
NOT_FOUND_ID_FLAG = "673773206d0e53d0d63f3341"
WRONG_ID_FLAG = "asd"

# MOCK MODES
TEST_MODE_NAME_MOCK = "Normal"
TEST_MODE_MOCK = {
    "_id": "673773206d0e53d0d63f3342",
    "description": "You must guess the most available flags in 10023 seconds.",
    "multiplier": 1000,
    "name": "Test",
    "timeleft": 2500
}
TEST_MODES_MOCK = [
    {
        "_id": "672687090bcd13f7c9a88ac3",
        "description": "You must guess the most available flags in 90 seconds.",
        "multiplier": 10,
        "name": "Normal",
        "timeleft": 90
    },
    {
        "_id": "6726874dde5266d8ba53ae77",
        "description": "You must guess the most available flags in 60 seconds.",
        "multiplier": 25,
        "name": "Hard",
        "timeleft": 60
    },
    {
        "_id": "67268757de5266d8ba53ae78",
        "description": "You must guess the most available flags in 25 seconds.",
        "multiplier": 100,
        "name": "Hardcore",
        "timeleft": 25
    }
]
NOT_FOUND_ID_MODE = "673773206d0e53d0d63f3342"
WRONG_ID_MODE = "asd"

# MOCK USERS
TEST_USER_MOCK = {
    "_id": "673773206d0e53d0d63f3343",
    "username": "DieTest",
    "password": "1234",
    "scores": {
        "general": 25,
        "normal": 25
    },
    "total_score": 25
}
TEST_USERS_MOCK = [
    {
        "_id": "673773206d0e53d0d63f3347",
        "username": "DieTest1",
        "password": "1234",
        "scores": {
            "general": 75,
            "normal": 75
        },
        "total_score": 75
    },
    {
        "_id": "673773206d0e53d0d63f3345",
        "username": "DieTest2",
        "password": "1234",
        "scores": {
            "general": 25,
            "normal": 25
        },
        "total_score": 25
    },
    {
        "_id": "673773206d0e53d0d63f3123",
        "username": "DieTest3",
        "password": "1234",
        "scores": {
            "general": 50,
            "normal": 50
        },
        "total_score": 50
    }
]
NOT_FOUND_ID_USER = "673773206d0e53d0d63f3343"
WRONG_ID_USER = "asd"

# MOCK ENCRYPT
PASSWORD="1234"
HASH_PASSWORD="scrypt:32768:8:1$BwWYLVJv3JX5lQk3$ce2b05aea5786c63b7815873557f086ddcc333f6ce1f473d17227be27d813cea704ae722c6ebc2f7bf3598b937bffb33152286bdb4b2e91a5323e6ac2784a0f5"