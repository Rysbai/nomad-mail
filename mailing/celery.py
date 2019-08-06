from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing.settings')

app = Celery('mailing')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.broker_url = 'amqp://otuzyhno:m8IstNKvaLlzZcoA2CS9EwXLKjtgBWtu@crocodile.rmq.cloudamqp.com/otuzyhno'
print(app.conf.broker_url)
app.conf.timezone = 'Asia/Bishkek'

app.conf.beat_schedule = {
    'check-distributions-send-time-every-three-hours': {
        'task': 'distribution.tasks.check_time_to_distribution',
        'schedule': crontab(minute='*/30'),
    },
}
