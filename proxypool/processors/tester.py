import asyncio
import sys
import aiohttp
import re
from pyquery import PyQuery as pq
from proxypool.storage.redisclient import redisClient
from aiohttp.client_exceptions import ClientConnectorError, ClientHttpProxyError, \
    ServerDisconnectedError, ClientOSError, ClientResponseError
from asyncio import TimeoutError
from proxypool.untils.parse import bytes_convert_string
from lxml.etree import ParserError, XMLSyntaxError
from proxypool.untils.loggings import Logging
from proxypool.setting import COUNT, REDIS_KEY, TEST_URL, TEST_URL_SWITCH, ip111
from requests.exceptions import ConnectionError
from urllib3.exceptions import MaxRetryError, NewConnectionError
from socket import gaierror

access_proxy = False        # 默认标记代理不可用
again_access_proxy = False  # 默认标记代理不可用

Exceptions = (
    ClientConnectorError,
    ClientHttpProxyError,
    ClientOSError,
    ServerDisconnectedError,
    TimeoutError,
    ClientResponseError,
    AssertionError,
    ParserError,
    XMLSyntaxError,
    ConnectionError,
    MaxRetryError,
    NewConnectionError,
    gaierror,
)


class Tester(object):
    """
    测试代理池
    """

    def __init__(self):
        self.redis = redisClient()
        self.logger = Logging()
        # https://github.com/aio-libs/aiohttp/issues/4536#issuecomment
        if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.loop = asyncio.get_event_loop()

    async def test(self, proxy):
        """
        测试每个代理状况
        :param: proxy,代理服务器，比如：`66.42.45.249:6666`

		ip111：默认不开启，从谷歌测试proxy是否用，True if available, Interface from `http://ip111.cn/`
		TEST_URL_SWITCH：默认开启，需配合TEST_URL测试，TEST_URL可自行配置，比如TEST_URL: `https://www.baidu.com`
        """
        global access_proxy, again_access_proxy
        try:
            async with aiohttp.ClientSession() as session:
                if ip111:
                    # 测试proxy是否可用，True if available, Interface from http://ip111.cn/
                    async with session.get(url='http://sspanel.net/ip.php', proxy=f'http://{proxy}', timeout=3) as response:
                        res_text = await response.text()
                        doc = pq(res_text).text()
                        match = re.search(r'(\d+\.\d+\.\d+\.\d+)', doc)
                        if match:
                            # access_proxy = match.group()
                            access_proxy = True

                # 获取当前主机公网ip
                async with session.get(url='https://www.httpbin.org/ip') as response:
                    res_json = await response.json()
                    origin_ip = res_json.get('origin', None)

                # 测试proxy是否可用，可用则返回proxy
                async with session.get(url='https://www.httpbin.org/ip', proxy=f'http://{proxy}', timeout=3) as response:
                    res_json = await response.json()
                    _proxy_ip = res_json.get('origin', None)

                # 断言判断
                assert origin_ip != _proxy_ip
                proxy_ip = proxy.split(":")[0]
                assert proxy_ip == _proxy_ip

                if TEST_URL_SWITCH:
                    # 测试proxy是否可访问测试url
                    async with session.get(TEST_URL, proxy=f'http://{proxy}', timeout=3) as response:
                        if response.status == 200:
                            again_access_proxy = True

                if access_proxy or again_access_proxy:
                    self.redis.max(REDIS_KEY, proxy)  # 设置最高分
                else:
                    self.redis.decrease(REDIS_KEY, proxy)  # 代理不可用则减分
        except Exceptions:
            self.redis.decrease(REDIS_KEY, proxy)  # 代理不可用则减分
            self.logger.debug(f'proxy {proxy} is invalid')

    @Logging.catch
    def run(self):
        self.logger.info('starting tester......')
        count = self.redis.get_count(REDIS_KEY)
        self.logger.debug(f'{count} proxies to test')
        cursor = 0
        while True:
            self.logger.debug(f'Testing proxies use cursor {cursor}, count {COUNT}')
            # 从redis中迭代获取集合元素,其中COUNT参数是：每次批量测试代理的个数
            cursor, proxies = self.redis.batch(REDIS_KEY, cursor, COUNT)
            if proxies:
                tasks = [self.test(bytes_convert_string(proxy[0])) for proxy in
                         proxies]
                self.loop.run_until_complete(asyncio.wait(tasks))
            if not cursor:
                break


#

def runtest():
    # 跳过redis测试单个代理是否可用
    proxy = '45.233.244.123:8083'
    tests = [tester.test(proxy)]
    tester.loop.run_until_complete(asyncio.wait(tests))


if __name__ == '__main__':
    tester = Tester()
    # tester.run()
    runtest()

