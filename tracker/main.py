from server import run_server
import asyncio
from tracker_config import Config
import sys

if __name__ == '__main__':
    args = sys.argv[1:]
    Config.SERVER_ADDRESS = args[0].split(':')[0]
    Config.SERVER_PORT = args[0].split(':')[1]

    asyncio.run(run_server(host=Config.SERVER_ADDRESS,
                           port=Config.SERVER_PORT))
