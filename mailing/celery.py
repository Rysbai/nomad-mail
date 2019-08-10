from __future__ import absolute_import, unicode_literals
import django

import datetime
import os
from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from django.conf import settings
from django.core.mail import get_connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing.settings')
django.setup()

app = Celery('mailing', backend='amqp', broker='amqp://')
app.config_from_object('django.conf:settings')

# app.conf.broker_url = settings.BROKER_URL
app.conf.timezone = 'Asia/Bishkek'
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


from distribution.models import Distribution
from distribution.tasks import give_messages


@app.task
@periodic_task(run_every=crontab(minute=30))
def check_time_to_distribution():

    distributions = Distribution.objects.filter(is_sent=False, send_date__lte=datetime.datetime.now())
    if distributions:
        connection = get_connection(fail_silently=False)
        connection.open()
        messages = give_messages(distributions)

        connection.send_messages(messages)
        connection.close()


# app.conf.beat_schedule = {
#     'checking_time_to_send_messages': {
#         'task': 'distribution.tasks.check_time_to_distribution',
#         'schedule': crontab(minute='*/30'),
#     },
# }
