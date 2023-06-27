import logging


class GetLogger:
    def __init__(self, log_level):
        self.log_level = log_level

    def get_logger(self, name):
        logger = logging.getLogger(f'python-KucRobot.{name}')
        logger.setLevel(level=self.log_level)
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        if not logger.handlers:
            logger.addHandler(console)
        return logger
