import logging


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level={
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'ERROR': logging.ERROR,
    }["INFO"])

logger = logging.getLogger()


class Log:
    def __init__(self):
        self.access_log = []


log = Log()
