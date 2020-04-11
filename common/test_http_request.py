import unittest
import logging
from common import my_logger
from ddt import ddt, data
from common.http_request import HttpRequest
from common.do_excel import DoExcel
from common import read_path
from common.do_mysql import DoMySql

test_data = DoExcel(read_path.test_data_path).get_test_data('test_data')
COOKIES = {}
LOAN_ID = ''
LOAN_MEMBER_ID = '23600'  # 存储借款用户的member_id
INVEST_MEMBER_ID = ''  # 存储投资用户的member_id
MOBILE_PHONE = ''  # 存储投资用户的手机号


@ddt
class TestHttpRequest(unittest.TestCase):
    def setUp(self):
        self.t = DoExcel(read_path.test_data_path)

    @data(*test_data)
    def test_api(self, item):
        global COOKIES
        global LOAN_ID
        global INVEST_MEMBER_ID
        global MOBILE_PHONE
        before_amount = ''
        logging.info('正在执行第{0}条用例：{1}'.format(item['Case_Id'], item['Title']))
        logging.info('发起请求的地址是：{0}'.format(item['Url']))

        # HTTP请求之前替换${loan_id}
        if item['Param'].find('${loan_id}') != -1:
            new_param = item['Param'].replace('${loan_id}', str(LOAN_ID))
            if item['Param'].find('${member_id}') != -1:
                new_param = new_param.replace('${member_id}', str(INVEST_MEMBER_ID))
        else:
            new_param = item['Param']
        logging.info('请求的参数是：{0}'.format(new_param))

        # HTTP请求之前获取用户余额
        if item['Case_Id'] in (14, 26, 41):
            sql_leave_amount = 'SELECT LeaveAmount FROM member WHERE MobilePhone = {0}'.format(MOBILE_PHONE)
            before_amount = int(DoMySql().do_my_sql(sql_leave_amount)[0])

        # HTTP请求
        response = HttpRequest().http_request(item['Url'], eval(new_param), item['Method'], COOKIES)
        res = response.json()

        # HTTP请求之后获取用户余额
        if item['Case_Id'] in (14, 26, 41):
            sql_leave_amount = 'SELECT LeaveAmount FROM member WHERE MobilePhone = {0}'.format(MOBILE_PHONE)
            after_amount = int(DoMySql().do_my_sql(sql_leave_amount)[0])
            if abs(before_amount - after_amount) == int(eval(new_param)['amount']):
                SQLCheckResult = 'PASS'
            else:
                SQLCheckResult = 'FAIL'
            self.t.write_back(item['Case_Id'] + 1, 10, SQLCheckResult)

        # HTTP请求之后根据手机号获取投资用户memberId
        if INVEST_MEMBER_ID == '':
            sql_member_id = 'SELECT id FROM member WHERE mobilephone={0}'.format(eval(item['Param'])['mobilephone'])
            member_id = DoMySql().do_my_sql(sql_member_id)[0]
            INVEST_MEMBER_ID = member_id

        # HTTP请求之后获取LOAN_ID
        # 第一种方法
        # if item['Param'].find('memberId') != -1:
        #     member_id = eval(item['Param'])['memberId']
        #     sql_loan_id = 'SELECT max(Id) FROM loan WHERE MemberID={0}'.format(member_id)
        #     LOAN_ID = DoMySql().do_my_sql(sql_loan_id)[0]
        # 第二种方法
        sql_loan_id = 'SELECT max(Id) FROM loan WHERE MemberID={0}'.format(LOAN_MEMBER_ID)
        loan_id = DoMySql().do_my_sql(sql_loan_id)[0]

        if loan_id:
            LOAN_ID = loan_id

        # 如果响应结果的cookies不为空，则把cookies更新进去
        if response.cookies != {}:
            COOKIES = response.cookies
            MOBILE_PHONE = eval(new_param)['mobilephone']

        try:
            self.assertEqual(str(item['Expected']), res['code'])
            test_result = 'PASS'
        except Exception as e:
            logging.error('出错了，错误是{0}'.format(e))
            test_result = 'FAIL'
            raise e
        else:
            logging.info('执行成功，结果是：{0}'.format(res))

        finally:
            self.t.write_back(item['Case_Id'] + 1, 8, str(res))
            self.t.write_back(item['Case_Id'] + 1, 9, test_result)

