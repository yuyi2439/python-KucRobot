import logging
import requests
import json
from main import log_level, http_addr

login_user_id = 0


def get_logger(name):
    logger = logging.getLogger(f'python-KucRobot.{name}')
    logger.setLevel(level=log_level)
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
    if not logger.handlers:
        logger.addHandler(console)
    return logger


def get_login_user_id():
    global login_user_id
    if login_user_id != 0:
        login_user_id = json.loads(requests.get(url=f'{http_addr}/get_login_info').content)['data']['user_id']
    return login_user_id
