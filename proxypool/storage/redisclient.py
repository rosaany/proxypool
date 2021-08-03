from redis import StrictRedis, ConnectionPool
from typing import Dict, List
from random import choice
from proxypool.untils.parse import bytes_convert_string
from proxypool.untils.loggings import Logging
from proxypool.setting import (REDIS_HOST,
                               REDIS_PORT,
                               REDIS_DB,
                               DEFAULT_SCORE,
                               MAX_SCORE,
                               MIN_SCORE,
                               REDIS_PASSWORD)


class redisClient(object):
    """
    Redis操作-增删改查：proxy
    """

    def __init__(self):
        self.redis = StrictRedis(host=REDIS_HOST,
                                 password=REDIS_PASSWORD,
                                 port=REDIS_PORT,
                                 db=REDIS_DB,
                                 decode_responses=True)
        self.logger = Logging()

    def add(self, redis_key, proxy, score=DEFAULT_SCORE) -> int:
        """
        添加代理
        args:
         - redis_key: 传入集合name
         - proxy: 传入以字典格式的IP代理，比如{'8.8.8.8:1080': 10}
        :return:
        """
        if isinstance(score, int) and proxy.strip():
            return self.redis.zadd(redis_key, {proxy: score})

    def decrease(self, redis_key, proxy):
        """
        对代理的分数做增减操作
        """
        self.redis.zincrby(redis_key, -1, proxy)
        current_score = self.redis.zscore(redis_key, proxy)
        self.logger.info(f"{proxy} current score {current_score}, decrease -1")
        if current_score <= 0:
            self.logger.info(f"{proxy} current score {current_score}, removing proxy")
            self.redis.zrem(redis_key, proxy)

    def max(self, redis_key, proxy, score=MAX_SCORE):
        """
        对可用代理设置最高分
        """
        self.logger.info(f'Modifying the ({proxy}) score to ({score})')
        return self.redis.zadd(redis_key, {proxy: score})

    def get_count(self, redis_key) -> int:
        """
        获取集合name所有的个数
        :param redis_key: 集合name
        :return:
        """
        return self.redis.zcard(redis_key)

    def get_all(self, redis_key, min_score=0, max_score=100, start=None, num=None, withscores=False) -> List:
        """
        根据指定分数范围获取集合name代理
        :param redis_key: 集合name
        :param min_score: 指定最小分数
        :param max_score: 指定最大分数
        :return:
        """
        if start is None:
            start = 0
        elif num is None:
            num = self.get_count(redis_key)
        return self.redis.zrangebyscore(redis_key, min_score, max_score, start, num, withscores)

    def exists(self, redis_key, proxy) -> bool:
        """
        判断代理是否存在，不存在返回True
        :param redis_key: 集合name
        :param proxy: value
        :return:
        """
        return self.redis.zscore(redis_key, proxy) == None

    def random_proxy(self, redis_key):
        """
        随机获取代理，优先获取获取最高分数的，其次再随机获取最低~最高分数之间的所有元素
        :param redis_key:
        :return:
        """
        high_score_proxies = self.redis.zrangebyscore(redis_key, MAX_SCORE, MAX_SCORE)
        if len(high_score_proxies):
            return bytes_convert_string(choice(high_score_proxies))
        low_to_high_score_proxies = self.redis.zrangebyscore(redis_key, MIN_SCORE, MAX_SCORE)
        if len(low_to_high_score_proxies):
            return bytes_convert_string(choice(low_to_high_score_proxies))
        self.logger.exception("no proxy")
        return None

    def batch(self, redis_key, cursor, count):
        """
        迭代有序集合元素
        """
        cursor, proxies = self.redis.zscan(redis_key, cursor=cursor, count=count)
        return cursor, proxies


if __name__ == '__main__':
    proxy = '1.2.4.8:1080'
    client = redisClient()
    client.add('proxy', proxy, score=100)
