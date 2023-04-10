from exceptions import *
import random


class Database:
    def __init__(self):
        self._data_nodes = {}

    def get_data(self, file_name):
        peer = self._data_nodes.get(file_name)
        if not peer:
            raise FileDoseNotExist(f'file with name {file_name} dose not exit on network')
        return peer

    def add_data(self, file_name, peer):
        if not self._data_nodes.get(file_name):
            self._data_nodes[file_name] = []
        self._data_nodes[file_name].append(peer)

    def remove_peer(self, file_name, peer):
        peers = self._data_nodes[file_name]
        peers.remove(peer)
        self._data_nodes[file_name] = peers

    def prune_peer(self, peer):
        for file_name in list(self._data_nodes):
            if peer in self._data_nodes[file_name]:
                self._data_nodes[file_name].remove(peer)

    def get_all_data(self):
        return self._data_nodes

    @staticmethod
    def chooseـpeer(peers):
        if len(peers) == 0:
            raise Exception('file dose not exist')
        return random.choice(peers)


database = Database()