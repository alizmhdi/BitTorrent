from server import run_server
import asyncio
from config import *
import sys

if __name__ == '__main__':
    args = sys.argv[1:]
    SERVER_ADDRESS = args[0].split(':')[0]
    SERVER_PORT = args[0].split(':')[1]

    asyncio.run(run_server(host=SERVER_ADDRESS,
                           port=SERVER_PORT))
