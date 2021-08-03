import requests
from loguru import logger


def get_proxy(proxy_url):
    """
    随机获取一个代理
    :return: 返回一个代理，比如：`1.2.4.8:6666`，如果没有找到代理则返回`{}`
    """
    try:
        res = requests.get(proxy_url).json()
        return res.get('proxy', None)
    except ConnectionError:
        logger.error('get proxy error')


def test_proxy(proxy):
    """
    测试一个代理
    :proxy: 传入一个代理，比如：`113.93.224.2:3256`
    """
    if not len(proxy):
        logger.error(f'没有获取到代理，请等待...')
    logger.debug(f'获得一个代理：{proxy} 正在测试是否可用...')
    try:
        res = requests.get('http://httpbin.org/get', proxies={'http': f'http://{proxy}'}, timeout=5)
        if res.status_code == 200:
            print(res.text)
            origin = res.json().get('origin')
            proxy_ip = proxy.split(":")[0]
            assert origin == proxy_ip
            logger.success("代理可用", f'{proxy_ip}')
    except Exception as e:
        logger.error(f'代理 {proxy} 失败 {e}')


if __name__ == '__main__':
    proxy_url = 'http://127.0.0.1:5555/random'
    proxy = get_proxy(proxy_url)
    test_proxy(proxy)
