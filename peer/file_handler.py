from config import *
from exceptions import *
from config import Config


class FileHandler:
    @staticmethod
    def get_file(file_name):
        try:
            file = open(Config.FILE_PATH + '/' + file_name, 'r')
        except Exception:
            raise FileDoseNotExist()
        return file.read()

    @staticmethod
    def write_file(file_name, content):
        file = open(Config.FILE_PATH + '/' + file_name + '1', 'w')
        file.write(content)
