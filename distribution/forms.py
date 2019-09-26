from django import forms

from distribution.models import Distribution
from event.models import get_countries_choices, get_countries_list

from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class SelectWidget(forms.Widget):
    template_name = 'distribution/select_widget.html'

    class Media:
        js = ('distribution/js/jquery.dropdown.js', )
        css = {
            'all': ('distribution/css/jquery.dropdown.css', )
        }

    def format_value(self, value):
        return value

    def render(self, name, value, attrs=None, renderer=None):
        if value:
            value = value.split(',')
        else:
            value = []

        context = {
            "values": get_countries_list(),
            "selected": value,
            "name": name,
            "id": "id_" + name
        }
        return mark_safe(render_to_string(self.template_name, context))


class DistributionCreateForm(forms.ModelForm):
    to_countries = forms.CharField(widget=SelectWidget())

    class Meta:
        model = Distribution
        fields = ['name', 'subject', 'body', 'to_sex', 'to_countries', 'for_event', 'send_date']


