from exceptions import *


class Database:
    def __init__(self):
        self._data_nodes = {}

    def get_data(self, file_name):
        peer = self._data_nodes.get(file_name)
        if not peer:
            raise FileDoseNotExist(f'file with name {file_name} dose not exit on network')
        return peer

    def add_data(self, file_name, peer_name, ip):
        if file_name in self._data_nodes.keys():
            raise FileAlreadyExist(f'file with name {file_name} already exits on network')
        self._data_nodes[file_name] = {
            'name': peer_name,
            'ip': ip
        }
