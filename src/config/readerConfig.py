from configparser import ConfigParser


class readerConfig:

    def __init__(self):
        self.parse = ConfigParser()
        self.parse.read('src\config\config.ini')
        # self.parse.read('../config.ini')

    def get_thehive_config(self):
        """
        :return: hive.url, hive.api config
        """
        return self.parse['thehive']
