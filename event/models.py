import os
from django.db import models

from event.constants import MAX_COL_CHAR, RECIPIENT_SEX_CHOICE, ALL_COUNTRIES
from event.utils import parse_xls, get_col_number


class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    excel_file = models.FileField(upload_to="event/", verbose_name='Excel с участниками')

    name_col = models.CharField(max_length=MAX_COL_CHAR, default='A', verbose_name='Имя')
    surname_col = models.CharField(max_length=MAX_COL_CHAR, default='B', verbose_name='Фамилия')
    birth_date_col = models.CharField(max_length=MAX_COL_CHAR, default='C', verbose_name='День рождения')
    sex_col = models.CharField(max_length=MAX_COL_CHAR, default='D', verbose_name='Пол')
    country_col = models.CharField(max_length=MAX_COL_CHAR, default='E', verbose_name='Страна')
    phone_col = models.CharField(max_length=MAX_COL_CHAR, default='F', verbose_name='Телефон')
    email_col = models.CharField(max_length=MAX_COL_CHAR, default='G', verbose_name='Email')
    distance_col = models.CharField(max_length=MAX_COL_CHAR, default='H', verbose_name='Дистанция')
    register_date_col = models.CharField(max_length=MAX_COL_CHAR, default='I', verbose_name='Дата регистрации')
    pay_status_col = models.CharField(max_length=MAX_COL_CHAR, default='J', verbose_name='Статус оплаты')

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self._past_excel_file = self.excel_file

        self.current_name_col = self.name_col
        self.current_surname_col = self.surname_col
        self.current_birth_date_col = self.birth_date_col
        self.current_sex_col = self.sex_col
        self.current_country_col = self.country_col
        self.current_phone_col = self.phone_col
        self.current_email_col = self.email_col
        self.current_distance_col = self.distance_col
        self.current_register_date_col = self.register_date_col
        self.current_pay_status_col = self.pay_status_col

    def save(self, *args, **kwargs):
        is_create = False
        if self._state.adding:
            is_create = True

        self._lowercase_columns()._strip_columns()
        super().save(*args, **kwargs)
        if is_create or self._is_columns_changed() or self.excel_file != self._past_excel_file:
            self._delete_recipients()
            self._create_recipients()
            self._delete_file()

    def _lowercase_columns(self):
        self.name_col = self.name_col.lower()
        self.surname_col = self.surname_col.lower()
        self.birth_date_col = self.birth_date_col.lower()
        self.sex_col = self.sex_col.lower()
        self.country_col = self.country_col.lower()
        self.phone_col = self.phone_col.lower()
        self.email_col = self.email_col.lower()
        self.distance_col = self.distance_col.lower()
        self.register_date_col = self.register_date_col.lower()
        self.pay_status_col = self.pay_status_col.lower()

        return self

    def _strip_columns(self):
        self.name_col = self.name_col.strip()
        self.surname_col = self.surname_col.strip()
        self.birth_date_col = self.birth_date_col.strip()
        self.sex_col = self.sex_col.strip()
        self.country_col = self.country_col.strip()
        self.phone_col = self.phone_col.strip()
        self.email_col = self.email_col.strip()
        self.distance_col = self.distance_col.strip()
        self.register_date_col = self.register_date_col.strip()
        self.pay_status_col = self.pay_status_col.strip()

    def _is_columns_changed(self):
        return self.name_col != self.current_name_col \
            or self.surname_col != self.current_surname_col \
            or self.birth_date_col != self.current_birth_date_col \
            or self.sex_col != self.current_sex_col \
            or self.country_col != self.current_country_col \
            or self.phone_col != self.current_phone_col \
            or self.email_col != self.current_email_col \
            or self.distance_col != self.current_distance_col \
            or self.register_date_col != self.current_register_date_col \
            or self.pay_status_col != self.current_pay_status_col

    def _delete_recipients(self):
        recipients = Recipient.objects.filter(event_id=self.id)
        for recipient in recipients:
            recipient.delete()

    def _create_recipients(self):
        for kwargs in parse_xls(self.excel_file.path, self._get_cols()):
            Recipient.objects.create(event_id=self.id, **kwargs).save()

    def _delete_file(self):
        os.remove(self.excel_file.path)

    def _get_cols(self):
        return {
            'surname': get_col_number(self.surname_col),
            'name': get_col_number(self.name_col),
            'birth_date': get_col_number(self.birth_date_col),
            'sex': get_col_number(self.sex_col),
            'country': get_col_number(self.country_col),
            'phone': get_col_number(self.phone_col),
            'email': get_col_number(self.email_col),
            'distance': get_col_number(self.distance_col),
            'register_date': get_col_number(self.register_date_col),
            'pay_status': get_col_number(self.pay_status_col)
        }

    def __str__(self):
        return self.name


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


def get_countries_choices():
    countries = [(ALL_COUNTRIES, "Все страны")]
    country_list = []
    recipients = Recipient.objects.all()

    for recipient in recipients:
        if recipient.country not in country_list:
            country_list.append(recipient.country)
            countries.append((recipient.country, recipient.country))

    return tuple(countries)
