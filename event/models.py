from django.db import models

from .parser import parse_xls


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
        if is_create:
            Recipient.create_mass_recipients(self.id, parse_xls(self.excel_file.path))
        elif self.excel_file != self._past_excel_file:
            Recipient.delete_recipients_by_event_id(self.id)
            Recipient.create_mass_recipients(self.id, parse_xls(self.excel_file.path))
            self._past_excel_file = self.excel_file

    def __str__(self):
        return self.name


RECIPIENT_SEX_CHOICE = (
    ('М', 'М'),
    ('Ж', 'Ж')
)


def get_countries_choices():
    countries = []
    country_list = []
    recipients = Recipient.objects.all()

    for recipient in recipients:
        if recipient.country not in country_list:
            country_list.append(recipient.country)
            countries.append((recipient.country, recipient.country))

    return tuple(countries)
    # return tuple()


class Recipient(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    name = models.CharField(max_length=200, verbose_name='Имя')
    surname = models.CharField(max_length=200, verbose_name='Фамилия')
    birth_date = models.CharField(max_length=200, verbose_name='Дата рождения')
    sex = models.CharField(choices=RECIPIENT_SEX_CHOICE, max_length=50, verbose_name='Пол')
    country = models.CharField(max_length=100, verbose_name='Страна')
    phone = models.CharField(max_length=200, verbose_name='Телефон')
    email = models.EmailField(max_length=200, verbose_name='Email')
    distance = models.CharField(max_length=100, verbose_name='Дистанция')
    register_date = models.CharField(max_length=100, verbose_name='Дата регистрации')
    pay_status = models.CharField(max_length=100, verbose_name='Статус оплаты')

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    @staticmethod
    def create_mass_recipients(event_id, args):
        for kwargs in args:
            Recipient.objects.create(event_id=event_id, **kwargs).save()

    @staticmethod
    def delete_recipients_by_event_id(event_id):
        recipients = Recipient.objects.filter(event_id=event_id)
        for recipient in recipients:
            recipient.delete()

    def __str__(self):
        return self.name + " " + self.surname
