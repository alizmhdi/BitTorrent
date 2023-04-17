import asyncudp
import socket
from config import Config
from file_handler import FileHandler
from logger import logger
import json


class Response:
    def __init__(self, message: str):
        params = message.split('\n')
        self.code = int(params[0])
        self.message = params[1]
        if self.code == 200:
            params[2] = params[2].replace("\'", "\"")
            self.data = json.loads(params[2])


class UDPClient:
    def __init__(self):
        self.host = Config.TRACKER_IP
        self.port = Config.TRACKER_PORT
        self.local_ip = Config.CLIENT_IP
        self.local_port = Config.CLIENT_PORT

    async def run_client(self, request: str):
        sock = await asyncudp.create_socket(remote_addr=(self.host, self.port))
        sock.sendto(request.encode())
        data, addr = await sock.recvfrom()
        sock.close()
        return data.decode()


class TCPClient:
    def __init__(self, remote_host, remote_port):
        self.host = remote_host
        self.port = remote_port
        self.local_ip = Config.CLIENT_IP
        self.local_port = Config.CLIENT_PORT

    async def parse_response(self, response: bytes, tracker_connection):
        params = response.split(b'\n')
        if params[0] == b'200':
            content = b'\n'.join(params[2:])
            FileHandler.write_file(params[1], content)
            logger.info('ok')
        else:
            logger.error(response)

    def send_message(self, message):
        s = socket.socket()
        s.connect((self.host, self.port))
        s.send(message.encode())
        response = s.recv(Config.BUFFER_SIZE)
        s.close()
        return response

