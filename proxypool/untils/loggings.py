import sys
import time
from loguru import logger
from pathlib import Path
from proxypool.setting import OPEN_LOG



class Logging(object):
    """
    日志记录
    """
    _instance = None
    _log = OPEN_LOG

    def __new__(cls, *arg, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *arg, **kwargs)
        return cls._instance

    def __init__(self):
        if self._log:
            self.log()

    def info(self, msg):
        return logger.info(msg)

    def debug(self, msg):
        return logger.debug(msg)

    def error(self, msg):
        return logger.error(msg)

    def exception(self, msg):
        return logger.exception(msg)

    @classmethod
    def catch(cls, func):
        @logger.catch
        def decorator(*args, **kwargs):
            return func(*args, **kwargs)

        return decorator

    def log(self):
        """
        项目下生成log
        """
        if self._log:
            t = time.strftime('%Y_%m_%d')
            present_path = sys.path[0]
            p = Path(present_path).resolve()
            log_path = p.joinpath('log')
            logger.add(f'{log_path}/crawl_{t}.log',
                       level='ERROR',
                       enqueue=True,
                       rotation='00:00',
                       retention='1 months',
                       compression='tar.gz',
                       encoding='utf-8',
                       backtrace=True)


if __name__ == '__main__':
    l = Logging()
