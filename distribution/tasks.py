from __future__ import absolute_import, unicode_literals

import datetime

from django.core.mail import EmailMultiAlternatives, get_connection
from django.template import loader, Template, Context
from mailing import settings

from mailing.celery import app
from distribution.models import Distribution


@app.task
def check_time_to_distribution():

    distributions = Distribution.objects.filter(is_sent=False, send_date__lte=datetime.datetime.now())
    if distributions:
        connection = get_connection(fail_silently=False)
        connection.open()
        messages = give_messages(distributions)

        connection.send_messages(messages)
        connection.close()


def give_messages(distributions):
    messages = []
    for distribution in distributions:
        for distribution_item in distribution.distributionitem_set.all():
            context = {
                "name": distribution_item.recipient.name,
                "surname": distribution_item.recipient.surname,
                "email": distribution_item.recipient.email,
                "distance": distribution_item.recipient.distance,
                "sex": distribution_item.recipient.sex,
                "country": distribution_item.recipient.country,
                "phone": distribution_item.recipient.phone,
            }
            html_email_template_name = "distribution/message.html"
            body = Template(distribution_item.distribution.body).render(Context(context))
            email_message = EmailMultiAlternatives(
                subject=''.join(distribution_item.distribution.subject.splitlines()),
                body=body,
                from_email=settings.EMAIL_HOST_USER,
                to=[distribution_item.recipient.email]
            )
            html_email = loader.render_to_string(
                html_email_template_name,
                {"message": body}
            )
            email_message.attach_alternative(html_email, 'text/html')
            messages.append(email_message)

            distribution_item.is_sent = True
            distribution_item.save()

        distribution.is_sent = True
        distribution.save()

    return messages
