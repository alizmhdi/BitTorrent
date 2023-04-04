import asyncudp
import socket
from config import *
from file_handler import FileHandler
from logger import logger
import json


class Response:
    def __init__(self, message: str):
        params = message.split()
        self.code = int(params[0])
        self.message = params[1]
        self.data = json .loads(params[2])


class UDPClient:
    def __init__(self, remote_address: str, port: int):
        self.host = remote_address
        self.port = port

    async def send_message(self, request: str):
        sock = await asyncudp.create_socket(remote_addr=(self.host, self.port))
        sock.sendto(request.encode())
        data, addr = await sock.recvfrom()
        sock.close()
        return data.decode()


tracker = UDPClient(TRACKER_IP, TRACKER_PORT)


class TCPClient:
    def __init__(self, remote_address: str, port: int):
        self.host = remote_address
        self.port = port

    @staticmethod
    def parse_response(response: str):
        params = response.split('\n')
        if params[0] == '200':
            content = '\n'.join(params[2:])
            FileHandler.write_file(params[1], content)
            tracker.send_message(f'share {params[1]} {CLIENT_IP}:{CLIENT_PORT}')
            logger.info('ok')
        else:
            logger.error(response)

    def send_message(self, message):
        s = socket.socket()

        s.connect((self.host, self.port))
        s.send('ack'.encode())

        s.send(message.encode())
        response = s.recv(BUFFER_SIZE).decode()
        TCPClient.parse_response(response)
        s.close()
        return response

