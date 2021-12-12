from celery import Celery
from celery.schedules import crontab
from crawler import DataCrawler
from celery.exceptions import SoftTimeLimitExceeded

app = Celery()
app.conf.broker_url = 'redis://redis'

app.conf.beat_schedule = {
    'crawl_every_1_hour': {
        'task': 'tasks.crawl',
        'schedule': crontab(hour='*/1')
    }
}


@app.task()
def crawl():
    try:
        DataCrawler().start()
        return 'crawl task done'
    except SoftTimeLimitExceeded:
        return 'task failed, time limit exceeded'
