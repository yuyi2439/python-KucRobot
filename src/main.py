import asyncio
import threading
import requests
import json
import logging
from utils import GetLogger

ws_addr = 'ws://localhost:8080'
http_addr = 'http://localhost:5700'
log_level = logging.DEBUG

version = '0.0.1'
connected = False


def parse(m):
    if m['post_type'] == 'message':
        if m['message_type'] == 'group':
            # 群消息
            plugins.msg_event('group', sub_type=m['sub_type'], msg_id=m['message_id'],
                              user_id=m['user_id'], msg=m['message'], group_id=m['group_id'],
                              anonymous=m['anonymous'])
        elif m['message_type'] == 'private':
            # 私聊消息
            plugins.msg_event('private', sub_type=m['sub_type'], msg_id=m['message_id'],
                              user_id=m['user_id'], msg=m['message'], temp_source=m['temp_source'])
        else:
            logger.debug(json.dumps(m))
    elif m['post_type'] == 'notice':
        if m['notice_type'] == 'group_increase':
            # 群成员增加
            pass
        elif m['notice_type'] == 'group_decrease':
            # 群成员减少
            pass
        elif m['notice_type'] == 'group_recall':
            # 消群消息撤回
            pass
        else:
            logger.debug(json.dumps(m))
    else:
        logger.debug(json.dumps(m))


def ws_connected():
    global login_user_id
    if not login_user_id:
        login_user_id = json.loads(requests.get(url=f'{http_addr}/get_login_info').content)['data']['user_id']


class InputThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            user_input = input()
            if user_input == 'reload':
                plugins.reload_plugins()
            # elif user_input == 'connect':
            #     if connected:
            #         logger.info('已经连接了，不能重复连接')
            #     else:
            #         await receive_event()
            else:
                logger.info('这不是一条指令')


if __name__ == '__main__':
    from plugins_manager import PluginManager

    get_logger = GetLogger(log_level).get_logger

    logger = get_logger('main')

    logger.info(f'python-KucRobot:{version}正在启动')
    plugins = PluginManager(get_logger)

    input_thread = InputThread()
    input_thread.start()

    asyncio.run(receive_event())
