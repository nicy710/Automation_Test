import os

# 项目文件路径
pro_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

# 配置文件路径
conf_path = os.path.join(pro_path, 'conf', 'pro.conf')

# 测试数据路径
test_data_path = os.path.join(pro_path, 'test_data', 'test_case.xlsx')

# 测试报告路径
test_report_path = os.path.join(pro_path, 'test_result', 'test_report', 'test_report.html')

# 测试log路径
log_path = os.path.join(pro_path, 'test_result', 'log', 'test_log.txt')