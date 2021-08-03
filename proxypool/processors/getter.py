from proxypool.crawler import classes
from proxypool.storage.redisclient import redisClient
from proxypool.untils.loggings import Logging
from proxypool.setting import REDIS_KEY


class Getter(object):

    def __init__(self):
        self.redis = redisClient()
        self.classes = [cls() for cls in classes]
        self.in_storage_count = 0
        self.logger = Logging()

    @Logging.catch
    def run(self):
        if len(self.classes):
            for cls in self.classes:
                self.logger.info(f'Get the proxy instance object: {cls}')
                for proxy in cls.crawl():
                    add_count = self.redis.add(REDIS_KEY, proxy)
                    self.in_storage_count += add_count
                self.logger.info(f"Number of redis in storage: {self.in_storage_count}")

if __name__ == '__main__':
    test = Getter()
    test.run()

