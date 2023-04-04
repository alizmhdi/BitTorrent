from exceptions import *


class Database:
    def __init__(self):
        self._data_nodes = {}

    def get_data(self, file_name):
        peer = self._data_nodes.get(file_name)
        if not peer:
            raise FileDoseNotExist(f'file with name {file_name} dose not exit on network')
        return peer[-1]

    def add_data(self, file_name, peer):
        if not self._data_nodes.get(file_name):
            self._data_nodes[file_name] = []
        self._data_nodes[file_name].append(peer)


database = Database()