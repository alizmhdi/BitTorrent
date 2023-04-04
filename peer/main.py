import sys
from config import Config
from clients import *
import asyncio
from server import PeerServer


def share(file_name, tracker):
    response = Response(
        asyncio.run(tracker.run_client(f'share {file_name} {Config.CLIENT_IP}:{Config.CLIENT_PORT}')))
    if response.code == 200:
        logger.info('ok share')
        asyncio.run(PeerServer.run_server())
    else:
        logger.error(response.message)


def get(file_name, tracker):
    response = Response(
        asyncio.run(tracker_connection.run_client(f'get {file_name} {Config.CLIENT_IP}:{Config.CLIENT_PORT}')))
    if response.code == 200:
        peer = response.data['peer'].split(':')
        peer = TCPClient(peer[0], int(peer[1]))
        response = peer.send_message(f'get {file_name}')
        peer.parse_response(response, tracker)
        share(file_name, tracker)
    else:
        logger.error(response.message)


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

    if method == 'get':
        get(file_name, tracker_connection)

    if method == 'share':
        share(file_name, tracker_connection)

