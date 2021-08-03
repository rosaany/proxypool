
from pyquery import PyQuery as pq
from proxypool.crawler.base import Base


class proxy_seofangfa(Base):
    url = 'https://proxy.seofangfa.com/'

    # proxies = {
    #     'http': 'http://127.0.0.1:1080',
    #     'https': 'https://127.0.0.1:1080',
    # }

    def parse(self, html):
        doc = pq(html)
        hosts = doc('.table td:nth-child(1)').text().split(' ')
        ports = doc('.table td:nth-child(2)').text().split(' ')
        for host, port in zip(hosts, ports):
            yield f'{host.strip()}:{port.strip()}'

if __name__ == '__main__':
    test = proxy_seofangfa()
    test.crawl()
