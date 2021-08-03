import json
from flask import Flask, g
from proxypool.storage.redisclient import redisClient
from flask import jsonify
from proxypool.untils.parse import bytes_convert_string
from proxypool.setting import REDIS_KEY

app = Flask(__name__)


@app.route("/")
def index():
    """
    首页
    访问入口`<host-ip>`
    """
    return "<h2>Index Page</h2>" \
           "<p>For example:</p>" \
           "<p>'<host:port>/random',Get a proxy random</p>" \
           "<p>'<host:port>./proxies',Get all proxy(including unavailable) a proxy format: ip:port,score</p>" \
           "<p>'<host:port>/proxy/<num>',Get <num> proxy(including unavailable)</p>"


@app.route("/random")
def get_proxy():
    """
    随机返回一个代理
    访问入口`<host-ip>/random`

    :return: 从redis中读取代理，如果读取失败则返回`{}`，如果读取成功则返回`{'proxy': proxy}`,比如proxy=59.55.164.6:3256
    """
    g.redis = redisClient() if not hasattr(g, 'redis') else g.redis
    g.proxy = g.redis.random_proxy(redis_key='proxies')
    if g.proxy is not None:
        return jsonify(proxy=g.proxy)
    return {'proxy': {}}


@app.route("/proxies")
@app.route("/proxy/<num>")
def get_count(num=None):
    """
    返回count个代理
    访问入口`<host-ip>/proxy/<count>`,其中count是用户输入的数字，输入多少返回多少，超过redis上限则返回all
    访问入口`<host-ip>/proxies`,返回所有代理
    """
    g.redis = redisClient() if not hasattr(g, 'redis') else g.redis
    all = g.redis.get_count(redis_key=REDIS_KEY)
    if num is None:
        # 当访问http://xxx/proxy时，返回all
        g.count = all
    else:
        # 否则只要输入的num不超过all，输入多少返回多少
        if int(num) > all:
            g.count = all
        else:
            g.count = num
    g.proxies = g.redis.get_all(redis_key=REDIS_KEY, start=0, num=g.count, withscores=True)
    p = {}
    for proxy in g.proxies:
        p[bytes_convert_string(proxy[0])] = str(proxy[1])  # for examples: (b'121.232.148.77:3256', 8.0)
    p = json.dumps(p)
    return jsonify(count=g.count, proxy=p)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555)
