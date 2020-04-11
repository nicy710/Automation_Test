import unittest
import HTMLTestRunnerNew

from common.test_http_request import TestHttpRequest
from common import read_path
from common.send_email import SendEmail


if __name__ == '__main__':
    # 收集测试用例
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TestHttpRequest))

    # 生成测试报告
    with open(read_path.test_report_path, 'wb+') as file:
        runner = HTMLTestRunnerNew.HTMLTestRunner(file, title='20180901测试报告', description='前程贷接口测试（一）', tester='小雅')
        runner.run(suite)

    # 添加发送邮件的请求
    # file_dic = {'test_report.html': read_path.test_report_path,
    #             'test_case.xlsx': read_path.test_data_path,
    #             'test_log.txt': read_path.log_path}
    # SendEmail().send_email('nicy710@163.com', file_dic)