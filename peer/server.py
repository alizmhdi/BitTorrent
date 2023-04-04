import asyncio
import socket
from config import *
from file_handler import FileHandler


class PeerServer:

    @staticmethod
    async def handle_client(client):
        loop = asyncio.get_event_loop()
        loop.sock_sendall(client, f'connected to peer {CLIENT_IP}:{CLIENT_PORT}'.encode())
        request = (await loop.sock_recv(client, 255)).decode('utf8').split()
        method = request[0]
        file_name = request[1]
        if method != 'get':
            response = '400\n' + file_name
        else:
            try:
                response = '200\n' + file_name + '\n' + FileHandler.get_file(file_name)
            except FileExistsError:
                response = '404\n' + file_name
        await loop.sock_sendall(client, response.encode('utf8'))
        client.close()

    @staticmethod
    async def run_server():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((CLIENT_IP, CLIENT_PORT))
        server.listen(MAX_LISTEN)
        server.setblocking(False)

        loop = asyncio.get_event_loop()

        while True:
            client, addr = await loop.sock_accept(server)
            loop.create_task(PeerServer.handle_client(client))
