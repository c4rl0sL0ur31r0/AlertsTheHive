
from datetime import datetime
import dateparser
import requests

from src.modules.hiveModules.hiveModules import hiveModules


class urlhausSpain:

    def __init__(self):
        self.target_url = 'https://urlhaus.abuse.ch/feeds/country/ES/'

    def urlFeed(self):
        response = requests.get(self.target_url)
        data = response.text
        alert_list = []
        for i, line in enumerate(data.split('\n')):

            if line.startswith('#'):
                pass
            else:
                artifact_alert = {}
                parserLine = line.split(',')
                if len(parserLine[0].replace('"', '')) > 0:
                    dateAdded = dateparser.parse(parserLine[0].replace('"', '')).date()
                    # if dateAdded is not None:
                    if dateAdded == datetime.today().date():
                        artifact_alert['dateAdded'] = dateAdded
                        artifact_alert['url'] = parserLine[1].replace('"', '')
                        artifact_alert['url_status'] = parserLine[2].replace('"', '')
                        artifact_alert['threat'] = parserLine[3].replace('"', '')
                        artifact_alert['host'] = parserLine[4].replace('"', '')
                        artifact_alert['ip'] = parserLine[5].replace('"', '')
                        artifact_alert['as_number'] = parserLine[6].replace('"', '')
                        artifact_alert['country'] = parserLine[7].replace('"', '')
                        print(artifact_alert)
                        alert_list.append(artifact_alert)
                    else:
                        pass
        return alert_list

    @staticmethod
    def create_alert():
        titleAlert = 'ESPAÑA MALWARE DROPPER {0}'.format(datetime.today().date())
        query_data = hiveModules().check_alert(title_alert=titleAlert)
        if query_data is not None:
            alert_ID = query_data
        else:
            alert_ID = hiveModules().create_alert(
                title_alert=titleAlert,
                tlp_alert='red',
                source_alert='urlhaus',
                severity_alert='high',
                description_alert='Alert from urlhaus spain',
                tags_alert=['malware dropper', 'Spain']
            )
        return str(alert_ID)

    def process(self):
        data_today = self.urlFeed()
        if len(data_today) > 0:
            alert_id = self.create_alert()
            for i in data_today:
                status_artifact = hiveModules().check_artifact(alert_ID=alert_id, artifact_compare=i['url'])
                if status_artifact is False:
                    hiveModules().create_artifact(
                        alert_id=alert_id,
                        type_artifact='url',
                        value_artifact=i['url'],
                        ioc_artifact=True
                    )
                if status_artifact is True:
                    pass
        else:
            pass