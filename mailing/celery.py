from __future__ import absolute_import, unicode_literals
import django

import re
import datetime
import os
import shutil
from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Template, loader, Context

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing.settings')
django.setup()

app = Celery('mailing', backend='amqp', broker='amqp://')
app.config_from_object('django.conf:settings')

app.conf.timezone = 'Asia/Bishkek'
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


from distribution.models import DistributionItem, Distribution, Counter

DAY_LIMIT = 3000
MONTH_FOR_DELETE_IMAGES = 6


def get_context(item):
    return Context({
        "name": item.recipient.name,
        "surname": item.recipient.surname,
        "email": item.recipient.email,
        "distance": item.recipient.distance,
        "sex": item.recipient.sex,
        "country": item.recipient.country,
        "phone": item.recipient.phone,
    })


def put_absolute_urls(text):
    pattern = r'<img[^>]+src="(/[^">]+)"'
    host = 'https://snowleopardrun.com'
    for src in re.findall(pattern, text):
        text = re.sub(src, host+src, text, count=1)

    return text


def send_messages():
    counter = Counter.objects.get(name='mail')
    html_email_template_name = "distribution/message.html"
    distribution_items = DistributionItem.objects.filter(
        distribution__is_sent=False,
        distribution__send_date__lte=datetime.datetime.now(),
        is_tried_send=False
    )
    index = 0
    items = []
    sequence_error = 0
    while index < len(distribution_items) and counter.count < DAY_LIMIT - 1:
        item = distribution_items[index]

        context = get_context(item)
        body = Template(
            put_absolute_urls(item.distribution.body)
        ).render(context)

        email_message = EmailMultiAlternatives(
            subject=''.join(item.distribution.subject.splitlines()),
            body=body,
            from_email=settings.EMAIL_HOST_USER,
            to=[item.recipient.email]
        )
        html_email = loader.render_to_string(
            html_email_template_name,
            {"message": body}
        )
        email_message.attach_alternative(html_email, 'text/html')
        try:
            email_message.send()
        except:
            item.is_tried_send = True
            item.save()
        else:
            item.is_tried_send = True
            item.is_sent = True
            item.save()
            counter.count += 1
        index += 1

    counter.save()


def close_sent_distributions():
    distributions = Distribution.objects.filter(is_sent=False, send_date__lte=datetime.datetime.now())
    for distribution in distributions:
        items = DistributionItem.objects.filter(distribution=distribution, is_tried_send=False)
        if not items:
            distribution.is_sent = True
            distribution.save()


@app.task
@periodic_task(run_every=crontab(minute=30))
def check_time_to_distribution():
    send_messages()
    close_sent_distributions()


@app.task
@periodic_task(run_every=crontab(minute=0, hour=0))
def send_didnt_send_distributions():
    counter = Counter.objects.get(name='mail')
    counter.count = 0
    counter.save()

    send_messages()
    close_sent_distributions()


@app.task
@periodic_task(run_every=crontab(day_of_month="1", hour=7, minute=30))
def delete_older_then_4_month_ckeditor_images():
    time = datetime.datetime.now() - datetime.timedelta(days=MONTH_FOR_DELETE_IMAGES * 31)
    year = str(time.year)
    month = str(time.month) if time.month >= 10 else "0" + str(time.month)
    directory = settings.MEDIA_ROOT + settings.CKEDITOR_UPLOAD_PATH + year + "/" + month
    try:
        shutil.rmtree(directory)
    except FileNotFoundError:
        pass
