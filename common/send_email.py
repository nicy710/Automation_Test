import smtplib
from email.mime.text import MIMEText    #专门发送正文
from email.mime.multipart import MIMEMultipart  #发送多个部分
from email.mime.application import MIMEApplication  #发送附件


class SendEmail:
    def send_email(self, send_to, send_file_dic):
        # 构造一个邮件体：正文  附件
        msg = MIMEMultipart()
        msg['Subject'] = '自动化测试报告'		# 主题
        msg['From'] = '875414271@qq.com'		# 发件人
        msg['To'] = send_to		# 收件人

        # 构造邮件正文
        part_text = MIMEText('这是自动化测试结果，请查收！')    # 正文
        msg.attach(part_text)   # 把正文加到邮件体里面去

        # 构建邮件附件
        for key, value in send_file_dic.items():
            part_attach = MIMEApplication(open(value, 'rb+').read())
            part_attach.add_header('Content-Disposition', 'attachment', filename=key)
            msg.attach(part_attach)

        # 发送邮件 smtp
        s = smtplib.SMTP_SSL('smtp.qq.com')	#连接服务器
        # 登录邮件服务器  密码：第三方授权码
        s.login('875414271@qq.com', 'pzjztmxdvwivbfej')
        s.sendmail('875414271@qq.com', send_to, msg.as_string())
        s.close()  #关闭连接


if __name__ == '__main__':
    from common import read_path
    file_dic = {'test_report.html': read_path.test_report_path,
                'test_case.xlsx': read_path.test_data_path,
                'test_log.txt': read_path.log_path}
    SendEmail().send_email('nicy710@163.com', file_dic)