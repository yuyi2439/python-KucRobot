class NoMsg(Exception):
    """
    Msg缺失错误
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'NoMsg'


class NoMsgId(Exception):
    """
    MsgId缺失错误
    """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'NoMsgId'


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
