import requests
import logging
from common import my_logger


class HttpRequest:
    def http_request(self, url, request_data, method, cookies):

        if method.lower() == 'get':
            try:
                res = requests.get(url, request_data, cookies=cookies)
            except Exception as e:
                logging.error('get请求出错了，错误是：{0}'.format(e))
                raise e
        elif method.lower() == 'post':
            try:
                res = requests.post(url, request_data, cookies=cookies)
            except Exception as e:
                logging.error('post请求出错了，错误是：{0}'.format(e))
                raise e
        else:
            return '参数方式错误'
        return res


if __name__ == '__main__':
    from common.get_cookies import GetCookies
    cookies = GetCookies().get_cookies()
    url = 'http://119.23.241.154:8080/futureloan/mvc/api/member/recharge'
    param = {'mobilephone': '17756894679', 'amount': '0'}
    res = HttpRequest().http_request(url, param, 'get', cookies)
    print(res)