# Generated by Django 2.2 on 2019-05-01 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residencia', '0002_auto_20190430_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='residencia',
            name='capacidad',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]