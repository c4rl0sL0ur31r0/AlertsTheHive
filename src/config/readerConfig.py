from configparser import ConfigParser


class readerConfig:

    def __init__(self):
        self.parse = ConfigParser()
        self.parse.read(r'C:\Users\ender\Desktop\c1b3rwallTaller23\src\config\config.ini')
        # self.parse.read('../config.ini')

    def get_thehive_config(self):
        """
        :return: hive.url, hive.api config
        """
        return self.parse['thehive']

#data = readerConfig().get_thehive_config()
#print(data['hive.url'], data['hive.api'])