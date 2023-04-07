from server import run_server
import asyncio
from tracker_config import Config
import sys
import threading
from logger import log
from database import database
from exceptions import *


def run_program():
    asyncio.run(run_server(host=Config.SERVER_ADDRESS,
                           port=Config.SERVER_PORT))


def keep_alive():
    pass


if __name__ == '__main__':
    args = sys.argv[1:]
    Config.SERVER_ADDRESS = args[0].split(':')[0]
    Config.SERVER_PORT = args[0].split(':')[1]

    x = threading.Thread(target=run_program)
    x.start()

    while True:
        command = input()
        if command == 'request logs':
            if len(log.access_log) == 0:
                print('There are no requests')
            else:
                for log in log.access_log:
                    print(log)
        if command == 'file_log -all':
            print(database.get_all_data())
            continue
        if command.startswith('file_log'):
            file = command.strip()[1]
            try:
                print(database.get_data(file))
            except FileDoseNotExist:
                print('this file dose not exist on tracker')
