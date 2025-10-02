import os


class Config:
    # General
    TZ = os.getenv("TZ", "America/Argentina/Buenos_Aires")

    # Mongo
    MONGO_URI = os.getenv("MONGO_URI")
    JSON_AS_ASCII = False

    # Flask
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 5000)
    DEBUG_MODE = os.getenv("DEBUG_MODE", False)
