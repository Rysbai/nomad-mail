from django import forms
from distribution.models import Distribution
from event.models import Recipient


RECIPIENT_SEX_CHOICE = (
    ('М', 'М'),
    ('Ж', 'Ж')
)


def get_countries():
    countries = []
    country_list = []
    recipients = Recipient.objects.all()

    for recipient in recipients:
        if recipient.country not in country_list:
            country_list.append(recipient.country)
            countries.append((recipient.country, recipient.country))

    return tuple(countries)


class DistributionCreateForm(forms.ModelForm):
    class Meta:
        model = Distribution
        fields = ['name', 'subject', 'body', 'send_date', 'event', 'sex', 'country']

        widgets = {
            "sex": forms.SelectMultiple(choices=RECIPIENT_SEX_CHOICE),
            "country": forms.SelectMultiple(choices=get_countries())
        }
