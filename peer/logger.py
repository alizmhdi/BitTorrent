import logging
from config import LOG_PATH

logging.basicConfig(
    filename=LOG_PATH,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level={
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'ERROR': logging.ERROR,
    }["INFO"])

logger = logging.getLogger()
