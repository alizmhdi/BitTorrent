import threading
import socket
from logger import logger
from exceptions import *
import json


class Server:
    def __init__(self, host='127.0.0.1', port=6771):
        logger.info(f'Initializing Server with host {host}, port {port}')
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((host, port))
            self.clients_list = {}
        except Exception as e:
            raise ServerInitializingFailed(str(e))

    def send_to_client(self, name, message):
        client_ip = self.clients_list.get(name)
        if not client_ip:
            raise ClientDoseNotExist(f'client with name {name} dose not exit.')
        try:
            self.sock.sendto(message, client_ip)
        except Exception as e:
            logger.error(str(e))

    def request_handler(self, request, client):
        data = json.loads(request)

    def listen_clients(self):
        while True:
            msg, client = self.sock.recvfrom(1024)
            logger.info('Received data from client %s: %s', client, msg)
            t = threading.Thread(target=self.request_handler, args=(msg, client,))
            t.start()
