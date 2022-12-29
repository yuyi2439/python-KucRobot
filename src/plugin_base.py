import error
import plugin_utils
import utils


class Utils:
    @staticmethod
    def send_group_msg(self, group_id, msg):
        """
        :return: 成功返回msg_id
        """
        return plugin_utils.send_group_msg(self, group_id, msg)

    @staticmethod
    def send_private_msg(self, user_id, msg):
        """
        :return: 成功返回msg_id
        """
        return plugin_utils.send_private_msg(self, user_id, msg)

    @staticmethod
    def get_msg(self, msg_id):
        """
        :return: 成功返回data
        """
        return plugin_utils.get_msg(self, msg_id)

    @staticmethod
    def delete_msg(self, msg_id):
        """
        :return: 成功返回data
        """
        return plugin_utils.delete_msg(self, msg_id)

    @staticmethod
    def get_logger(self):
        """
        :return: 成功返回logger对象
        """
        return utils.get_logger(f'{self.name}:{self.version}')


class NoMsg(error.NoMsg):
    """
    Msg缺失错误
    """
    def __init__(self):
        super().__init__()


class NoMsgId(error.NoMsgId):
    """
    MsgId缺失错误
    """
    def __init__(self):
        super().__init__()