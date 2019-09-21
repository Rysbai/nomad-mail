from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from multiselectfield import MultiSelectField

from event.models import Recipient, RECIPIENT_SEX_CHOICE, Event, get_countries_choices


class Distribution(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    subject = models.CharField(max_length=200, verbose_name='Тема')
    body = RichTextUploadingField(verbose_name='Сообщение')
    send_date = models.DateTimeField(verbose_name='Дата отправки')
    is_sent = models.BooleanField(default=False, verbose_name='Отправлено')

    to_sex = MultiSelectField(choices=RECIPIENT_SEX_CHOICE, verbose_name='Пол')
    to_countries = MultiSelectField(choices=get_countries_choices(), verbose_name='Страны')
    for_event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __init__(self, *args, **kwargs):
        super(Distribution, self).__init__(*args, **kwargs)
        self.current_to_sex = self.to_sex
        self.current_to_countries = self.to_countries
        try:
            self.current_for_event = self.for_event
        except:
            pass

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_create = False
        if self._state.adding \
            or self.current_to_sex != self.to_sex \
            or self.current_to_countries != self.to_countries \
            or self.current_for_event != self.for_event:

            is_create = True

        super().save(*args, **kwargs)

        if is_create:
            self._delete_all_items()
            self._create_dist_items()

    def _delete_all_items(self):
        distribution_items = self.distributionitem_set.all()
        for item in distribution_items:
            item.delete()

    def _create_dist_items(self):
        recipients = Recipient.objects.filter(
            event_id=self.for_event.id,
            sex__in=self.to_sex,
            country__in=self.to_countries
        )
        for recipient in recipients:
            DistributionItem.objects.create(distribution_id=self.id, recipient_id=recipient.id).save()


class DistributionItem(models.Model):
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE, verbose_name='Рассылка')
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, verbose_name='Получатель')
    try_count = models.IntegerField(default=0)
    is_sent = models.BooleanField(default=False, verbose_name='Отправлено')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.recipient.email


class Counter(models.Model):
    name = models.CharField(max_length=200)
    count = models.PositiveIntegerField(default=0)
