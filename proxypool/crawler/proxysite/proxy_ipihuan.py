from pyquery import PyQuery as pq
from proxypool.crawler.base import Base


class proxy_ipihuan(Base):
    url = 'https://ip.ihuan.me/'
    isvalid = False

    def parse(self, html):
        doc = pq(html)
        hosts = doc('.table td:nth-child(1)').text().split(' ')
        ports = doc('.table td:nth-child(2)').text().split(' ')
        for host, port in zip(hosts, ports):
            yield f'{host.strip()}:{port.strip()}'


if __name__ == '__main__':
    test = proxy_ipihuan()
    test.crawl()
