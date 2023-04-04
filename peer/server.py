import asyncio
import socket
from config import Config
from file_handler import FileHandler
from logger import logger


class PeerServer:

    @staticmethod
    async def handle_client(client):
        loop = asyncio.get_event_loop()
        request = (await loop.sock_recv(client, 255)).decode('utf8').split()
        print(request)
        method = request[0]
        file_name = request[1]
        if method != 'get':
            response = '400\n' + file_name
        else:
            try:
                response = '200\n' + file_name + '\n' + FileHandler.get_file(file_name)
            except FileExistsError:
                response = '404\n' + file_name
        print(response)
        await loop.sock_sendall(client, response.encode('utf8'))
        client.close()

    @staticmethod
    async def run_server():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((Config.CLIENT_IP, Config.CLIENT_PORT))
        server.listen(Config.MAX_LISTEN)
        server.setblocking(False)

        loop = asyncio.get_event_loop()

        while True:
            client, addr = await loop.sock_accept(server)
            logger.info(f'connected {addr}!')
            loop.create_task(PeerServer.handle_client(client))
