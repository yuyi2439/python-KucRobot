import requests
import json
from main import http_addr
from error import NoMsg, NoMsgId

class Utils:
    def __init__(self, get_logger):
        self.logger = get_logger('plugins_collection')
    @staticmethod
    def send_group_msg(self, group_id, msg):
        """
        :return: 成功返回msg_id
        """
        if msg != '':
            params = {"group_id": group_id, "message": msg}
            r = requests.get(url=http_addr + '/send_group_msg', params=params)
            d = json.loads(r.content)
            if d['status'] == 'ok':
                msg_id = d['data']['message_id']
                return msg_id
            else:
                wording = d['wording']
                logger.warning(f'插件 {self.name} 向群 {group_id} 发送消息 {msg} 失败, wording: {wording}')
        raise NoMsg

    @staticmethod
    def send_private_msg(self, user_id, msg):
        """
        :return: 成功返回msg_id
        """
        if msg != '':
            params = {"user_id": user_id, "message": msg}
            r = requests.get(url=http_addr + '/send_private_msg', params=params).content
            d = json.loads(r)
            if d['status'] == 'ok':
                msg_id = d['data']['message_id']
                return msg_id
            else:
                wording = d['wording']
                logger.warning(f'插件 {self.name} 向用户 {user_id} 发送消息 {msg} 失败, wording: {wording}')
        raise NoMsg

    @staticmethod
    def get_msg(self, msg_id):
        """
        :return: 成功返回data
        """
        if msg_id != '':
            params = {"message_id": msg_id}
            r = requests.get(url=http_addr + '/get_msg', params=params).content
            d = json.loads(r)
            if d['status'] == 'ok':
                return d['data']
            else:
                wording = d['wording']
                logger.warning(f'插件 {self.name} 获取消息 {msg_id} 失败，wording: {wording}')
        raise NoMsgId

    @staticmethod
    def delete_msg(self, msg_id):
        """
        :return: 成功返回data
        """
        if msg_id != '':
            params = {"message_id": msg_id}
            r = requests.get(url=http_addr + '/delete_msg', params=params).content
            d = json.loads(r)
            if d['status'] == 'ok':
                return d['data']
            else:
                wording = d['wording']
                logger.warning(f'插件 {self.name} 撤回消息 {msg_id} 失败, wording: {wording}')
        raise NoMsgId
