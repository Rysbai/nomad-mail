import os
from django.db import models

from event.parser import parse_xls


class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    excel_file = models.FileField(upload_to="event/", verbose_name='Excel с участниками')

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self._past_excel_file = self.excel_file

    def save(self, *args, **kwargs):
        is_create = False
        if self._state.adding:
            is_create = True

        super().save(*args, **kwargs)
        if is_create or self.excel_file != self._past_excel_file:
            self._delete_recipients()
            self._create_recipients()
            self._delete_file()

    def _delete_recipients(self):
        recipients = Recipient.objects.filter(event_id=self.id)
        for recipient in recipients:
            recipient.delete()

    def _create_recipients(self):
        for kwargs in parse_xls(self.excel_file.path):
            Recipient.objects.create(event_id=self.id, **kwargs).save()

    def _delete_file(self):
        os.remove(self.excel_file.path)

    def __str__(self):
        return self.name


RECIPIENT_SEX_CHOICE = (
    ('М', 'М'),
    ('Ж', 'Ж')
)
ALL_COUNTRIES = "ALL"


def get_countries_choices():
    countries = [(ALL_COUNTRIES, "Все страны")]
    country_list = []
    recipients = Recipient.objects.all()

    for recipient in recipients:
        if recipient.country not in country_list:
            country_list.append(recipient.country)
            countries.append((recipient.country, recipient.country))

    return tuple(countries)


class Recipient(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    name = models.CharField(max_length=200, verbose_name='Имя', null=True)
    surname = models.CharField(max_length=200, verbose_name='Фамилия', null=True)
    birth_date = models.CharField(max_length=200, verbose_name='Дата рождения', null=True)
    sex = models.CharField(choices=RECIPIENT_SEX_CHOICE, max_length=50, verbose_name='Пол')
    country = models.CharField(max_length=100, verbose_name='Страна')
    phone = models.CharField(max_length=200, verbose_name='Телефон')
    email = models.EmailField(max_length=200, verbose_name='Email')
    distance = models.CharField(max_length=100, verbose_name='Дистанция',  null=True)
    register_date = models.CharField(max_length=100, verbose_name='Дата регистрации', null=True)
    pay_status = models.CharField(max_length=100, verbose_name='Статус оплаты', null=True)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return self.name + " " + self.surname
