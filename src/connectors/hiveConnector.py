import sys

from thehive4py.api import TheHiveApi
from thehive4py.models import Version

from src.config.readerConfig import readerConfig


class hiveConnector:
    def __init__(self):
        hive_config = readerConfig().get_thehive_config()
        self.url_hive = hive_config['hive.url']
        self.token_hive = hive_config['hive.api']
        self.version_hive = Version.THEHIVE_4.value

    def connect(self):

        api_hive = TheHiveApi(
            self.url_hive,
            self.token_hive,
            version=self.version_hive
        )
        if api_hive.health().status_code == 200:
            return api_hive
        else:
            print('ERROR')
            sys.exit()


