from pyquery import PyQuery as pq
from proxypool.crawler.base import Base


class proxy_89ip(Base):
    url = 'https://www.89ip.cn/index_1.html'

    def parse(self, html):
        doc = pq(html)
        hosts = doc('.layui-table td:nth-child(1)').text().split(' ')
        ports = doc('.layui-table td:nth-child(2)').text().split(' ')
        for host, port in zip(hosts, ports):
            yield f'{host.strip()}:{port.strip()}'


if __name__ == '__main__':
    test = proxy_89ip()
    test.crawl()