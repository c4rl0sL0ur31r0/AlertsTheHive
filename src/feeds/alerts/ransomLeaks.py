import requests
import dateparser
from datetime import datetime
import warnings

from src.modules.hiveModules.hiveModules import hiveModules

warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)


class ransomLeaks:
    def __init__(self):
        self.posts = 'https://raw.githubusercontent.com/joshhighet/ransomwatch/main/posts.json'
        self.posts_data = requests.get(url=self.posts)

    def get_posts(self):
        list_return = []
        for i in self.posts_data.json():
            date_parse = str(dateparser.parse(i['discovered']).date())
            if date_parse == str(datetime.today().date()):
                attack_parser = {}
                attack_parser['group_name'] = i['group_name']
                attack_parser['title'] = i['post_title']
                attack_parser['date'] = date_parse
                list_return.append(attack_parser)
        return list_return

    @staticmethod
    def create_alert():
        titleAlert = 'Ransomware Leaks {0}'.format(datetime.today().date())
        query_data = hiveModules().check_alert(title_alert=titleAlert)
        if query_data is not None:
            alert_ID = query_data
        else:
            alert_ID = hiveModules().create_alert(
                title_alert=titleAlert,
                tlp_alert='red',
                source_alert='ransomwatch',
                severity_alert='high',
                description_alert='Alert from ransomware leaks',
                tags_alert=['ransomware']
            )
        return str(alert_ID)

    def process(self):
        data_today = self.get_posts()
        alert_id = self.create_alert()
        for i in data_today:
            status_artifact = hiveModules().check_artifact(alert_ID=alert_id, artifact_compare=i['title'])
            if status_artifact is False:
                hiveModules().create_artifact(
                    alert_id=alert_id,
                    type_artifact='url',
                    value_artifact=i['title'],
                    ioc_artifact=True,
                    tag_target=['{0}'.format(i['group_name'])]
                )
            if status_artifact is True:
                pass
