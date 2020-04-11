import logging
from common import read_path

# 指定日志输出位置
fh = logging.FileHandler(read_path.log_path, encoding='utf-8')  # 输出到文件
sh = logging.StreamHandler()  # 输出到控制台

# 指定日志输出格式
formatter = '%(asctime)s-%(levelname)s-%(filename)s-日志信息:%(message)s'
# 日期格式
dfmt = '%a, %d %b %Y %H:%M:%S'
logging.basicConfig(level=logging.DEBUG, handlers=[fh, sh], format=formatter, datefmt=dfmt)