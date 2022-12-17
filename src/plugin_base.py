import logging
from src.error import NoStartEvent
from utils import send_group_msg, send_private_msg, get_msg, delete_msg


class Plugin:
    """
    该基类每个插件都需要继承，插件需要实现基类定义的方法
    """
    def __init__(self):
        """
        插件的基础信息
        日志初始化
        """
        try:
            self.name
            self.version
        except NameError:
            self.name = 'unknown'
            self.version = 'unknown'
        self.logger = logging.getLogger(f'__main__.{self.name}:{self.version}')

    def start_event(self):
        """
        实际执行插件所初始化的方法
        """
        raise NoStartEvent

    async def group_msg_event(self, sub_type, msg_id, user_id, msg, group_id, anonymous, reply_msg_id: int):
        """
        :param sub_type: 消息子类型, 正常消息是 normal, 匿名消息是 anonymous, 系统提示是 notice, 回复消息是 reply
        :param msg_id: 消息 ID
        :param user_id: 发送者 QQ 号
        :param msg: 消息内容
        :param group_id: 群号
        :param anonymous: 匿名信息, 如果不是匿名消息则为 null
        :param reply_msg_id: 当sub_type为reply时, 为本消息所回复的消息的msg_id, 否则为0
        """

    async def private_msg_event(self, sub_type, msg_id, user_id, msg, *temp_source):
        """
        :param sub_type: 消息子类型, 正常消息是 normal, 匿名消息是 anonymous, 系统提示是 notice, 回复消息是 reply
        :param msg_id: 消息 ID
        :param user_id: 发送者 QQ 号
        :param msg: 消息内容
        :param temp_source: 临时会话来源
        """
