class NoMsg(Exception):
    """
    Msg缺失错误

    type: 发送消息的类型, 1为群消息, 2为私聊消息
    """
    def __init__(self, type: int, plugin_name, id, msg, wording):
        super().__init__()
        self.type = type
        self.plugin_name = plugin_name
        self.id = id
        self.msg = msg
        self.wording = wording

    def __str__(self):
        if self.type == 1:
            return f'插件 {self.plugin_name} 向群 {self.id} 发送消息 {self.msg} 失败, wording: {self.wording}'
        if self.type == 2:
            return f'插件 {self.plugin_name} 向用户 {self.id} 发送消息 {self.msg} 失败, wording: {self.wording}'


class NoMsgId(Exception):
    """
    MsgId缺失错误

    type: 1为获取消息, 2为撤回消息
    """
    def __init__(self, type: int, plugin_name, msg_id, wording):
        super().__init__()
        self.type = type
        self.plugin_name = plugin_name
        self.msg_id = msg_id
        self.wording = wording

    def __str__(self):
        if self.type == 1:
            return f'插件 {self.plugin_name} 获取消息 {self.msg_id} 失败，wording: {self.wording}'
        if self.type == 2:
            return f'插件 {self.plugin_name} 撤回消息 {self.msg_id} 失败，wording: {self.wording}'


class NoStartEvent(Exception):
    """
    插件无start_event错误
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'NoStartEvent'


class MsgTypeError(Exception):
    """
    消息类型错误
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'MsgTypeError'
