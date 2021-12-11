from celery import Celery
from celery.schedules import crontab
from crawler import DataCrawler

app = Celery()
app.conf.broker_url = 'redis://redis'

app.conf.beat_schedule = {
    'crawl_every_1_hour': {
        'task': 'tasks.crawl',
        'schedule': crontab(minute='*/2')
    }
}


@app.task()
def crawl():
    d = DataCrawler()
    d.start()
    return 'task done'
