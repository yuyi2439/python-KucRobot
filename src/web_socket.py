class WebSocket:
    def __init__(self, addr, parser):
        self.addr = addr
        self.parser = parser
        self.connected = False

    def connect(self):
        async def receive_event():
            logger.info(f'连接WebSocket中')
            try:
                async with websockets.connect(ws_addr) as w:
                    logger.info(f'连接 {ws_addr} 成功，正在获取消息')
                    connected = True

                    async for m in w:
                        msg = json.loads(m)
                        if msg['post_type'] != 'meta_event':
                            parse(msg)
            except websockets.exceptions.ConnectionClosedError:
                logger.warning('ws连接断开了，正在尝试重连')
                await receive_event()
            except ConnectionRefusedError:
                logger.error('ws连接失败，请检查ws地址配置，并确认go-cqhttp是否正确运行')
