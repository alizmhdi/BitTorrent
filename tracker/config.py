from decouple import config

LOG_PATH = config("LOG_PATH", "./log/tracker.log")
SERVER_ADDRESS = config("ADDRESS", "")
SERVER_PORT = config("PORT", 6771)
