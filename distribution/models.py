from django.db import models
from ckeditor.fields import RichTextField
from event.models import Recipient


class Distribution(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    subject = models.CharField(max_length=200, verbose_name='Тема')
    body = RichTextField(verbose_name='Сообщение')
    send_date = models.DateTimeField(verbose_name='Дата отправки')
    is_sent = models.BooleanField(default=False, verbose_name='Отправлено')
    rec_ids = models.TextField(verbose_name='Не трогайте!')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_create = False
        if self._state.adding:
            is_create = True
        super().save(*args, **kwargs)

        if is_create:
            DistributionItem.create_mass_dis_items(self.id, self.rec_ids.split(','))

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
            print(rec_id)
            try:
                DistributionItem.objects.create(
                    distribution_id=distribution_id,
                    recipient_id=rec_id
                )
            except:
                pass

    def __str__(self):
        return self.recipient.email
