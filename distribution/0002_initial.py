from django.db import migrations


def add_mail_counter(apps, schema_editor):
    Counter = apps.get_model('distribution', 'Counter')

    counter = Counter.objects.create(name='mail')
    counter.save()


class Migration(migrations.Migration):
    dependencies = [
        ('distribution', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_mail_counter),
    ]
