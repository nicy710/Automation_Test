import requests
from common.do_excel import DoExcel
from common import read_path


class GetCookies:
    def get_cookies(self):
        test_data = DoExcel(read_path.test_data_path, 'test_data').get_test_data()
        for item in test_data:
            if item['Module'] == 'login' and item['Title'] == '正常登陆':
                login_data = item
                if login_data['Method'].lower() == 'get':
                    try:
                        res = requests.get(login_data['Url'], eval(login_data['Param']))
                    except Exception as e:
                        print('出错了，错误是：{0}'.format(e))
                        raise e
                elif login_data['Method'].lower() == 'post':
                    try:
                        res = requests.post(login_data['Url'], eval(login_data['Param']))
                    except Exception as e:
                        print('出错了，错误是：{0}'.format(e))
                        raise e
                return res.cookies


if __name__ == '__main__':
    a = GetCookies().get_cookies()
    print(a)