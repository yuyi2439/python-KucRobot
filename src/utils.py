import requests
import json
import logging
from main import http_addr, msg_sender
from error import NoMsg, NoMsgId

logger = logging.getLogger('__main__.plugins_collection')


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
            msg_sender[msg_id] = self
            return msg_id
        else:
            raise NoMsg(1, self.name, group_id, msg, d['wording'])


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
            msg_sender[msg_id] = self
            return msg_id
        else:
            raise NoMsg(2, self.name, user_id, msg, d['wording'])


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
            raise NoMsgId(1, self.name, msg_id, d['wording'])


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
            raise NoMsgId(2, self.name, msg_id, d['wording'])
