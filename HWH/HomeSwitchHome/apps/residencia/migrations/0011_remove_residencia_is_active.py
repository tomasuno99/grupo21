# Generated by Django 2.2.1 on 2019-05-19 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('residencia', '0010_residencia_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='residencia',
            name='is_active',
        ),
    ]
