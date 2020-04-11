import configparser


class ReadConfig:
    def read_config(self, file_name, section, option):
        """读取配置文件里面的数据"""
        cf = configparser.ConfigParser()
        cf.read(file_name, encoding='utf-8')
        value = cf.get(section, option)
        return value
