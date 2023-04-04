import sys
from config import *
from clients import *


def get(file_name):
    response = Response(tracker.send_message(f'get {file_name} {CLIENT_IP}:{CLIENT_PORT}'))
    if response.code == 200:
        peer = response.data['peer'].split(':')
        peer = TCPClient(peer[0], int(peer[1]))
        response = peer.send_message(f'get file_name')
        TCPClient.parse_response(response)

    else:
        logger.error(response.message)

def share(file_name):
    response = Response(tracker.send_message(f'share {file_name} {CLIENT_IP}:{CLIENT_PORT}'))
    if response.code == 200:
        logger.info('ok share')
    else:
        logger.error(response.message)


if __name__ == "__main__":
    args = sys.argv[1:]
    method = args[0]
    file_name = args[1]
    tracker = args[0].split(':')
    client = args[1].split(':')
    TRACKER_IP = tracker[0]
    TRACKER_PORT = int(tracker[1])
    CLIENT_IP = client[0]
    CLIENT_PORT = int(client[1])

    if method == 'get':
        get(file_name)

    if method == 'share':
        share(file_name)

