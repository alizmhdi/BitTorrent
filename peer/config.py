from decouple import config

LOG_PATH = config("LOG_PATH", "./log/peer.log")
TRACKER_IP = config("TRACKER_IP", "127.0.0.1")
TRACKER_PORT = config("TRACKER_PORT", 6772)
CLIENT_IP = config("CLIENT_IP", "127.0.0.1")
CLIENT_PORT = config("CLIENT_PORT", 52612)
BUFFER_SIZE = config("BUFFER_SIZE", 1500)
FILE_PATH = config("FILE_PATH", "./files")
MAX_LISTEN = config("MAX_LISTEN", 10)