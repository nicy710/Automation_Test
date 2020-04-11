import mysql.connector
from common.read_config import ReadConfig
from common import read_path


class DoMySql:
    def do_my_sql(self, sql, state=1):
        config = eval(ReadConfig().read_config(read_path.conf_path, 'MYSQL', 'config'))
        cnn = mysql.connector.connect(**config)
        cursor = cnn.cursor()
        cursor.execute(sql)
        if state == 1:
            res = cursor.fetchone()#返回的数据类型是元组
        else:
            res = cursor.fetchall()#返回的数据类型是列表,里面的元素是元组
        cursor.close()
        cnn.close()
        return res

    def get_mobile_list(self):
        """获取所有已注册的手机号列表"""
        sql = 'select MobilePhone from member'
        a = self.do_my_sql(sql, 0)
        mobile_list = []
        for item in a:
            mobile = int(item[0])
            mobile_list.append(mobile)
        return mobile_list


if __name__ == '__main__':
    sql_max_tel = 'select max(mobilephone) from member'
    tel = int(DoMySql().do_my_sql(sql_max_tel, 1)[0]) + 1
    print(tel)

