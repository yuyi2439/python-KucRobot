import logging
from main import log_level


def get_logger(name):
    logger = logging.getLogger(f'python-KucRobot.{name}')
    logger.setLevel(level=log_level)
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
    if not logger.handlers:
        logger.addHandler(console)
    return logger
