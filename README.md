## proxypool

缩减版的代理池。

完整版参考：https://github.com/Python3WebSpider/ProxyPool

#### 常规环境
>Python >3.7
> 
>Redis

#### 安装依赖包

> pip3 install -r requirements.txt -i https://pypi.douban.com/simple

如需虚拟环境，创建一个[venv](https://docs.python.org/3/tutorial/venv.html)虚拟环境

> python3 -m venv proxypool


#### 运行代理池

> python3 run.py


运行后会分别启动Tester、Getter、Server，对应分别是检测模块、获取模块、接口模块。

单独运行某个模块
> python3 run.py --processor getter
>
> python3 run.py --processor tester
>
> python3 run.py --processor server

#### 配置项 (setting.py文件)
* redis配置

REDIS_HOST      # redis主机

REDIS_PORT      # redis端口号

REDIS_PASSWORD  # redis密码

REDIS_DB        # redis数据，0~15

DEFAULT_SCORE   # 默认分数，每个代理检测次数,不可用则-1,直至到0抛弃

MAX_SCORE       # 设置最高得分

MIN_SCORE       # 设置最低得分

REDIS_KEY       # redis集合name

COUNT           # 一次批量测试代理个数

* requests配置参数

TIMEOUT         # 请求超时时间

VERIFY          # 忽略证书

ENCODING        # 响应编码类型


* retry配置参数

stop_max_attempt_number              # 请求重试代理网站次数

wait_exponential_multiplier          # 最小请求时间

wait_exponential_max                 # 请求最大时间

* Flask配置

HOST          # Flask监听地址
  
PORT          # Flask监听端口   

*  核心模块开关

RUN_GETTER    # 获取模块             

RUN_TESTER    # 测试模块

RUN_SERVER    # 接口模块

* 其它配置

GETTER_CYCLE                       # 获取模块下一轮启动时间（单位/s)

TESTER_CYCLE                       # 获取模块下一轮启动时间（单位/s)

ip111                              # 是否启用此网址验证代理是否可用（使用站点'http://ip111.cn'检测）

TEST_URL_SWITCH                    # 是否启用测试网址验证代理是否可用 (使用站点'https://www.baidu.com'检测）

TEST_URL                           # 代理测试URL

OPEN_LOG                           # 是否开启日志记录，默认不开启

LEVEL                              # 日志级别(INFO, ERROR)
  



