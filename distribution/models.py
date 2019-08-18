import ast

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from event.models import Recipient, Event


def filter_recipients(event, sex, countries):
    return Recipient.objects.filter(event_id=event.id, sex__in=sex, country__in=countries)


class Distribution(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    subject = models.CharField(max_length=200, verbose_name='Тема')
    body = RichTextUploadingField(verbose_name='Сообщение')
    send_date = models.DateTimeField(verbose_name='Дата отправки')
    is_sent = models.BooleanField(default=False, verbose_name='Отправлено')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    sex = models.CharField(max_length=20, verbose_name='Пол')
    country = models.CharField(max_length=400, verbose_name='Страны')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __init__(self, *args, **kwargs):
        super(Distribution, self).__init__(*args, **kwargs)
        self._current_event_id = self.event_id
        self._current_sex = self.sex
        self._current_countries = self.country

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_create = False
        if self._state.adding:
            is_create = True
        super().save(*args, **kwargs)

        if is_create \
                or self.event_id != self._current_event_id \
                or self.sex != self._current_sex \
                or self.country != self._current_countries:

            self._current_event_id = self.event_id
            self._current_sex = self.sex
            self._current_countries = self.country

            country_list = ast.literal_eval(self.country)
            self.delete_all_items()
            for recipient in filter_recipients(self.event, self.sex, country_list):
                DistributionItem.objects.create(distribution_id=self.id, recipient=recipient).save()

    def delete_all_items(self):
        distribution_items = self.distributionitem_set.all()
        for item in distribution_items:
            item.delete()


class DistributionItem(models.Model):
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE, verbose_name='Рассылка')
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, verbose_name='Получатель')
    is_sent = models.BooleanField(default=False, verbose_name='Отправлено')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    @staticmethod
    def create_mass_dis_items(distribution_id, recipient_ids):
        for rec_id in recipient_ids[:-1]:
            try:
                DistributionItem.objects.create(
                    distribution_id=distribution_id,
                    recipient_id=rec_id
                )
            except:
                pass

    def __str__(self):
        return self.recipient.email


class Counter(models.Model):
    name = models.CharField(max_length=200)
    count = models.PositiveIntegerField(default=0)
