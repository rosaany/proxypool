import requests
from fake_headers import Headers
from retrying import retry
from proxypool.untils.parse import is_valid_proxy
from proxypool.processors.tester import Exceptions
from proxypool.setting import TIMEOUT, VERIFY, ENCODING, \
    stop_max_attempt_number, wait_exponential_multiplier, \
    wait_exponential_max
try:
    from proxypool.untils.loggings import Logging
    logging = Logging()
except ImportError:
    from loguru import logger as logging

class Base(object):
    """
    一个通用请求抓取代理网站类

    Instance variable:
    - :url:              # 爬取的url，也就是代理网站
    - :proxies:          # 使用代理 (可单独在子类配置，也就是抓取代理网站代码中配置）
    - :isvalid = True    # 标识代理网站是否可用，如果为False，则重新启动程序时，这个代理网站会被屏蔽掉，不再去请求

    decorator:
    - @retry(...):             # 一个装饰器，完成重复请求代理网站操作，具体的配置可在setting.py文件中配置，说明retry_on_result参数，x is None，
                            触发重试条件，即website_response函数的返回值
    """
    url = ""
    proxies = None
    isvalid = False

    def __init__(self):
        # 忽略安全警告
        requests.packages.urllib3.disable_warnings()
        self.logger = logging

    @retry(stop_max_attempt_number=stop_max_attempt_number, retry_on_result=lambda x: x is None,
           wait_exponential_multiplier=wait_exponential_multiplier,
           wait_exponential_max=wait_exponential_max)
    def website_response(self, url, **kwargs):
        """
        一个通用请求方法

        Args:
        - :url:             # 爬取的代理网站地址
        - kwargs:           # 使用kwargs定制一些配置

        Other variables:
        - headers           # 反爬虫伪装，如果无法安装fake_headers包（可能被国内墙了），可以手动构造一个headers.
        					示例：
                            headers = {'Accept': '*/*', 'Connection': 'keep-alive',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4;
                            rv:52.7.3) Gecko/20100101Firefox/52.7.3', 'DNT': '1',
                            'Referer': 'https://google.com', 'Pragma': 'no-cache'}

        - proxies           # 开启代理，如开启本地代理：
                            proxies = {
                                'http': 'http://127.0.0.1:1080',
                                'https': 'https://127.0.0.1:1080',
                            }


        """
        try:
            headers = Headers(headers=True).generate()
            kwargs.setdefault('timeout', TIMEOUT)
            kwargs.setdefault('verify', VERIFY)  # verify: Defaults to ``True``.
            kwargs.setdefault('headers', headers)
            # 爬取的代理网站是否加入代理去爬取
            if self.proxies is not None:
                kwargs.setdefault('proxies', self.proxies)
            res = requests.get(url, **kwargs)
            # 代理网站http响应码=200认为它正常
            if res.status_code == 200:
                res.encoding = ENCODING
                return res.text
        except Exceptions:
            return None

    @logging.catch
    def crawl(self):
        """
        一个抓取代理网站方法
            1.先是调用self.website_response实例方法，得到response.text赋值给html
            2.然后调用子类写好的parse爬取方法，也就是每一个代理网站的各自维护的抓取逻辑
            3.接着调用is_valid_proxy方法校验ip有效性，符合条件才会返回，否则返回None
            4.最后通过yield关键字返回代理
        """
        url = self.url
        self.logger.info(f'Request URL:{url}')
        html = self.website_response(url)
        for proxy in self.parse(html):
            proxy = is_valid_proxy(proxy)
            if proxy is not None:
                self.logger.info(f"Fetching proxy: {proxy} from {url}")
                yield proxy

