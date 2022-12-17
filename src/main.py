import asyncio
import threading
import requests
import websockets.client
import json
import logging

ws_addr = 'ws://localhost:8080'
http_addr = 'http://localhost:5700'
version = '0.0.1'

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
console = logging.StreamHandler()
console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
logger.addHandler(console)

msg_sender = {}
login_user_id = json.loads(requests.get(url=f'{http_addr}/get_login_info').content)['data']['user_id']


async def receive_event():
    logger.debug(f'连接WebSocket中')
    try:
        async with websockets.connect(ws_addr) as w:
            logger.info(f'连接 {ws_addr} 成功，正在获取消息')
            async for m in w:
                msg = json.loads(m)
                if msg['post_type'] != 'meta_event':
                    logger.debug(m)
                    await parse(msg)
    except websockets.exceptions.ConnectionClosedError as e:
        logger.error(f'websockets.exceptions.ConnectionClosedError {e}')
        await receive_event()


async def parse(m):
    if m['post_type'] == 'message':
        if m['message_type'] == 'group':
            await my_plugins.msg_event('group', sub_type=m['sub_type'], msg_id=m['message_id'],
                                       user_id=m['user_id'], msg=m['message'], group_id=m['group_id'],
                                       anonymous=m['anonymous'])
        elif m['message_type'] == 'private':
            try:
                m['temp_source']
            except KeyError:
                m['temp_source'] = ''
            await my_plugins.msg_event('private', sub_type=m['sub_type'], msg_id=m['message_id'],
                                       user_id=m['user_id'], msg=m['message'], temp_source=m['temp_source'])


class InputThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            user_input = input()
            if user_input == 'reload plugins':
                my_plugins.reload_plugins()
            else:
                logger.info(f'这不是一条指令')


if __name__ == '__main__':
    from plugins_collection import PluginCollection

    logger.info(f'kuc_robot:{version}正在启动')
    my_plugins = PluginCollection('plugins')

    input_thread = InputThread()
    input_thread.start()

    asyncio.run(receive_event())
