# Generated by Django 2.2.1 on 2019-05-20 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residencia', '0011_remove_residencia_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='residencia',
            name='imagen',
            field=models.CharField(default='', max_length=200),
        ),
    ]
