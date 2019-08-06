from django.db import models

from .parser import parse_xls


class Event(models.Model):
    name = models.CharField(max_length=200)
    excel_file = models.FileField(upload_to="event/")

    def save(self, *args, **kwargs):
        is_create = False
        if self._state.adding:
            is_create = True

        super().save(*args, **kwargs)
        if is_create:
            Recipient.create_mass_recipients(self.id, parse_xls(self.excel_file.path))

    def __str__(self):
        return self.name


RECIPIENT_SEX_CHOICE = (
    ('М', 'М'),
    ('Ж', 'Ж')
)


class Recipient(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    birth_date = models.CharField(max_length=200)
    sex = models.CharField(choices=RECIPIENT_SEX_CHOICE, max_length=50)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    distance = models.CharField(max_length=100)
    register_date = models.CharField(max_length=100)
    pay_status = models.CharField(max_length=100)

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
