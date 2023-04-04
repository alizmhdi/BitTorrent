import asyncio
from logger import logger
from database import database
import json
from exceptions import *


class Response:
    def __init__(self, code: str, message: str, data: dict = None):
        self.code = code
        self.message = message
        self.data = data

    def __str__(self):
        return f'{self.code} {self.message} \n {str(self.data)}'


class Request:
    def __init__(self, message: str):
        try:
            params = message.split()
            self.method = params[0]
            self.file_name = params[1]
            self.host = params[2]
        except Exception as e:
            raise BadRequestFormat()
        if self.method != 'get' and self.method != 'share':
            raise BadRequestFormat()


class UDPServer:
    @staticmethod
    def parse_request(message: str):
        try:
            request = Request(message)
            if request.method == 'get':
                peer = database.get_data(request.file_name)
                return Response(code=200,
                                message="ok",
                                data={'peer': peer})
            if request.method == 'share':
                database.add_data(file_name=request.file_name,
                                  peer=request.host)
                return Response(code=200,
                                message='ok',
                                data={})
        except BadRequestFormat:
            return Response(code='400',
                            message='bad request format')
        except FileDoseNotExist:
            return Response(code='404',
                            message='file dose not exist on network')

    def connection_made(self, transport):
        self.transport = transport

    async def send_to_client(self, address: str, response: Response):
        message = f'{response.code}\n{response.message}\n{str(response.data)}'
        await asyncio.sleep(0.5)
        self.transport.sendto(message.encode(), address)

    def datagram_received(self, data, address):
        logger.info(f'get request: {data} from {address}')

        response = UDPServer.parse_request(data.decode())
        loop = asyncio.get_event_loop()
        loop.create_task(self.send_to_client(address=address,
                                             response=response))


async def run_server(host, port):
    try:
        loop = asyncio.get_running_loop()
        await loop.create_datagram_endpoint(
            lambda: UDPServer(),
            local_addr=(host, port)
        )
    except Exception as e:
        raise ServerInitializingFailed(f'server dose not initial on {host}:{port} with error {str(e)}')

    logger.info(f'server listen on {host}:{port}')
    while True:
        await asyncio.sleep(3600)
