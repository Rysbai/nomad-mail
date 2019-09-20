from django import forms
from distribution.models import Distribution


class DistributionCreateForm(forms.ModelForm):
    class Meta:
        model = Distribution
        fields = ['name', 'subject', 'body', 'to_sex' , 'to_countries', 'for_event', 'send_date']
