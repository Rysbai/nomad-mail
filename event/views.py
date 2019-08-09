import json

from django.http import HttpResponse
from event.models import Event, Recipient


def get_events(request):
    queryset = Event.objects.all().order_by('-id')
    data = []
    for event in queryset.all():
        data.append({
                'id': event.id,
                'name': event.name
            })

    return HttpResponse(json.dumps(data), content_type='application/json')


def get_all_participants_country(request):
    countries = []
    country_list = []
    recipients = Recipient.objects.all()

    for recipient in recipients:
        if recipient.country not in country_list:
            country_list.append(recipient.country)
            countries.append({
                "name": recipient.country
            })

    return HttpResponse(json.dumps(countries), content_type='application/json')


def get_all_distances(request):
    distances = []
    data = []
    queryset = Recipient.objects.all()

    for recipient in queryset:
        if recipient.distance not in distances:
            distances.append(recipient.distance)
            data.append({
                "distance": recipient.distance
            })

    return HttpResponse(json.dumps(data), content_type='application/json')


def get_recipients(request):
    event_id = request.GET.get("event_id", None)
    sex = request.GET.get("sex", None)
    countries = request.GET.get("countries", None)

    if len(sex) > 1:
        sex = sex.split(',')

    if countries:
        countries = countries.split(',')
        queryset = Recipient.objects.filter(event_id=event_id, sex__in=sex, country__in=countries)
    else:
        queryset = Recipient.objects.filter(event_id=event_id, sex__in=sex)

    data = []
    for recipient in queryset:
        data.append(
            {
                "id": recipient.id,
                "name": recipient.name,
                "surname": recipient.surname,
                "distance": recipient.distance,
                "country": recipient.country,
                "sex": recipient.sex,
                "email": recipient.email
            }
        )

    return HttpResponse(json.dumps(data), content_type='application/json')


def get_recipients_by_ids(request):
    ids = request.GET.get("rec_ids", None).split(',')[:-1]
    queryset = Recipient.objects.filter(id__in=ids)

    event_id = None
    recipients = []
    countries = []
    sex = []
    for recipient in queryset:
        recipients.append(
            {
                "id": recipient.id,
                "name": recipient.name,
                "surname": recipient.surname,
                "distance": recipient.distance,
                "country": recipient.country,
                "sex": recipient.sex,
                "email": recipient.email
            }
        )
        event_id = recipient.event_id
        if recipient.country not in countries:
            countries.append(recipient.country)

        if recipient.sex not in sex:
            sex.append(recipient.sex)

    data = {
        "event_id": event_id,
        "countries": countries,
        "sex": sex,
        "recipients": recipients
    }
    return HttpResponse(json.dumps(data), content_type='application/json')
