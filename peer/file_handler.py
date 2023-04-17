from exceptions import *
from config import Config


class FileHandler:
    @staticmethod
    def get_file(file_name):
        try:
            file = open(Config.FILE_PATH + '/' + file_name, 'rb')
        except Exception:
            raise FileDoseNotExist()
        return file.read()

    @staticmethod
    def write_file(file_name, content):
        file = open(Config.FILE_PATH + '/1' + file_name.decode(), 'wb')
        file.write(content)
