from decouple import config


class Config:
    LOG_PATH = config("LOG_PATH", "./log/tracker.log")
    SERVER_ADDRESS = config("ADDRESS", "127.0.0.1")
    SERVER_PORT = config("PORT", 6771)
