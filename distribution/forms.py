from django import forms
from distribution.models import Distribution


class DistributionCreateForm(forms.ModelForm):
    class Meta:
        model = Distribution
        fields = ['name', 'subject', 'body', 'send_date', 'rec_ids']
