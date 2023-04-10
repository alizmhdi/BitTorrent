import sys
from clients import *
import asyncio
from server import PeerServer
import os
import sched, time
from logger import log
import threading


async def alive():
    while True:
        await tracker_connection.run_client(f'alive alive {Config.CLIENT_IP}:{Config.CLIENT_PORT}')
        await asyncio.sleep(5)


def run_alive():
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(10, 1, alive, (my_scheduler,))
    my_scheduler.run()


async def share(file_name, tracker):
    response = Response(
        await tracker.run_client(f'share {file_name} {Config.CLIENT_IP}:{Config.CLIENT_PORT}'))
    if response.code == 200:
        logger.info('ok share')
        loop = asyncio.get_event_loop()
        loop.create_task(alive())
        await asyncio.sleep(1)
        await PeerServer.run_server()
    else:
        logger.error(response.message)


async def get(file_name, tracker):
    response = Response(
        await tracker_connection.run_client(f'get {file_name} {Config.CLIENT_IP}:{Config.CLIENT_PORT}'))
    if response.code == 200:
        peer = response.data['peer'].split(':')
        peer = TCPClient(peer[0], int(peer[1]))
        response = peer.send_message(f'get {file_name} {Config.CLIENT_IP}:{Config.CLIENT_PORT}')
        await peer.parse_response(response, tracker)
        await share(file_name, tracker)
    else:
        logger.error(response.message)


def input_command():
    while True:
        command = input()
        if command == 'request logs':
            if len(log.access_log) == 0:
                print('There are no requests')
            else:
                for l in log.access_log:
                    print(l)


if __name__ == "__main__":
    args = sys.argv[1:]
    method = args[0]
    file_name = args[1]
    tracker = args[2].split(':')
    client = args[3].split(':')
    Config.TRACKER_IP = tracker[0]
    Config.TRACKER_PORT = int(tracker[1])
    Config.CLIENT_IP = client[0]
    Config.CLIENT_PORT = int(client[1])

    tracker_connection = UDPClient()

    x = threading.Thread(target=input_command)
    x.start()

    if method == 'get':
        asyncio.run(get(file_name, tracker_connection))

    if method == 'share':
        if os.path.isfile(Config.FILE_PATH + '/' + file_name):
            asyncio.run(share(file_name, tracker_connection))
        else:
            print('you have not this file')


