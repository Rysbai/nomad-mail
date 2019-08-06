from __future__ import absolute_import, unicode_literals
import django

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing.settings')
django.setup()

app = Celery('mailing')
app.config_from_object('django.conf:settings')

app.conf.broker_url = settings.BROKER_URL
app.conf.timezone = 'Asia/Bishkek'
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'distribution.tasks.check-distributions-send-time-every-three-hours': {
        'task': 'check_time_to_distribution',
        'schedule': crontab(minute='*/30'),
    },
}
