
import uuid
from thehive4py.models import *
from thehive4py.query import *

from src.connectors.hiveConnector import hiveConnector


class hiveModules:

    def __init__(self):

        self.api_hive = hiveConnector().connect()

    @staticmethod
    def __alertTlpSeverity(tlp_alert=None, severity_alert=None):
        tlpAlert = Tlp[tlp_alert.upper()].value
        severityAlert = Severity[severity_alert.upper()].value

        return tlpAlert, severityAlert

    def search_alert(self, title_search):
        """
        Alert search by title
        :param title_search:
        :return:
        """
        query = Like('title', title_search)
        response_query = self.api_hive.find_alerts(query=query)
        return response_query.json()

    def get_Artifacts(self, id_alert):
        response = self.api_hive.get_alert(alert_id=id_alert)
        alert_data = response.json()
        result_data = None
        if 'artifacts' in alert_data.keys():
            result_data = alert_data['artifacts']

        return result_data

    def check_artifact(self, alert_ID, artifact_compare):
        """
        Check if artifact in Alert Exist
        :param alert_ID:
        :param artifact_compare:
        :return:
        """
        artifacts = self.get_Artifacts(id_alert=alert_ID)
        exists_data = False
        if artifacts is not None:
            for artifact in artifacts:
                if artifact_compare == artifact['data']:
                    exists_data = True
        return exists_data

    def check_alert(self, title_alert=None):
        """
        check if alert exists
        :param title_alert:
        :return:
        """
        query_data = self.search_alert(title_search=title_alert)
        alert_ID = None
        if len(query_data) != 0:
            alert_search = query_data[0]
            alert_ID = alert_search['id']
        return alert_ID

    def create_alert(self, tlp_alert=None, severity_alert=None, title_alert=None, tags_alert=None,
                     description_alert=None, source_alert=None):
        """
        Create Hive Alert
        :param tlp_alert:
        :param severity_alert: example high
        :param title_alert:
        :param tags_alert: dict tags for alert
        :param description_alert:
        :param source_alert:
        :return:
        """

        sourceRef = str(uuid.uuid4())[0:6]
        tlpData = self.__alertTlpSeverity(tlp_alert=tlp_alert, severity_alert=severity_alert)
        alert = Alert(title=title_alert,
                      tlp=tlpData[0],
                      severity=tlpData[1],
                      tags=tags_alert,
                      description=description_alert,
                      type='IntelCon_Monitor',
                      source=source_alert,
                      sourceRef=sourceRef
                      )
        try:
            response = self.api_hive.create_alert(alert)
            alertData = response.json()
            return alertData['id']

        except Exception as e:
            print("Alert create error: {}".format(e))

    def create_artifact(self, type_artifact=None, value_artifact=None, ioc_artifact=False,
                        alert_id=None, tag_target=None):
        """
        Add artifact Hive Alert/Case
        :param type_artifact:
        :param value_artifact:
        :param ioc_artifact:
        :param alert_id:
        :param tag_target:
        :return:
        """
        artifact = AlertArtifact(dataType=type_artifact, data=value_artifact, ioc=ioc_artifact, tags=tag_target)
        self.api_hive.create_alert_artifact(alert_id, artifact)
