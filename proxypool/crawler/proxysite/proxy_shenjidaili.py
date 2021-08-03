from pyquery import PyQuery as pq
from proxypool.crawler.base import Base


class proxy_shenjidaili(Base):
    url = 'http://www.shenjidaili.com/product/open/'

    isvalid = True

    def parse(self, html):
        doc = pq(html)
        proxies = doc('.table td:nth-child(1)').text().split(' ')
        for proxy in proxies:
            yield f'{proxy}'


if __name__ == '__main__':
    test = proxy_shenjidaili()
    test.crawl()
