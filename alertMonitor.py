import schedule
import time
from src.feeds.alerts.urlhausSpain import urlhausSpain
from src.feeds.alerts.ransomLeaks import ransomLeaks


def job():
    urlhausSpain().process()
    ransomLeaks().process()


schedule.every(15).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
