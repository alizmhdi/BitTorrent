from server import run_server
import asyncio
from config import *

if __name__ == '__main__':
    asyncio.run(run_server(host=SERVER_ADDRESS,
                           port=SERVER_PORT))
