# Generated by Django 2.2.1 on 2019-07-13 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserva', '0007_hotsale'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='in_hotsale',
            field=models.BooleanField(default=False),
        ),
    ]
