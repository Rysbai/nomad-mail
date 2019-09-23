from django import forms

from event.constants import CODES
from event.models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'

    def clean(self):
        if self.is_columns_not_in_english():
            raise forms.ValidationError('Обозначения столбцев должны быть английскими буквами.')
        return self.cleaned_data

    def is_columns_not_in_english(self):
        columns = [
            self.cleaned_data.get('name_col'), self.cleaned_data.get('surname_col'),
            self.cleaned_data.get('birth_date_col'), self.cleaned_data.get('sex_col'),
            self.cleaned_data.get('country_col'), self.cleaned_data.get('phone_col'),
            self.cleaned_data.get('email_col'), self.cleaned_data.get('distance_col'),
            self.cleaned_data.get('register_date_col'), self.cleaned_data.get('pay_status_col')
        ]
        for col in columns:
            for char in col:
                if char.lower() not in CODES.keys():
                    return True

        return False

