# Generated by Django 2.0.13 on 2019-06-10 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reserva', '0004_auto_20190608_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subasta',
            name='is_deleted',
        ),
    ]
