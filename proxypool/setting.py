import platform

######################
# redis configure
######################
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_PASSWORD = 'Aa123456'
REDIS_DB = '0'

# redis ordered set
DEFAULT_SCORE = 10  # 默认分数，每个代理检测次数,不可用则-1,直至到0抛弃
MAX_SCORE = 20  # 代理最高得分
MIN_SCORE = 0  # 代理最低得分
REDIS_KEY = 'proxies'  # redis key

# redis batch
COUNT = 10  # 一次批量测试代理个数

#####################
# request configure
#####################
TIMEOUT = 10  # 请求超时时间
VERIFY = False  # 忽略证书
ENCODING = 'utf-8'  # 响应编码类型

######################
# retry configure
######################
# 请求重试代理网站次数
stop_max_attempt_number = 2
wait_exponential_multiplier = 1000
wait_exponential_max = 10000  # 请求最大时间

######################
# Flask configure
######################
HOST = "0.0.0.0"
PORT = 5555

#####################
# other configure
#####################
# 获取模块和检测模块分别各自执行完一轮，再次启动执行周期（单位/s)
GETTER_CYCLE = 200
TESTER_CYCLE = 10

# 是否启动一次验证代理是否用（使用站点'http://ip111.cn'检测）
ip111 = False

# 代理测试URL
TEST_URL = 'https://www.baidu.com'
# 是否启用二次验证代理可用 (使用站点'https://www.baidu.com'检测）
TEST_URL_SWITCH = True

# 核心模块开关
RUN_GETTER = True
RUN_TESTER = True
RUN_SERVER = True


###############################
# 是否开启log
###############################
OPEN_LOG = True
