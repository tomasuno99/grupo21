# Generated by Django 2.1.7 on 2019-05-19 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_premium',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='semanas_disponibles',
            field=models.PositiveSmallIntegerField(blank=True, default=2, null=True),
        ),
    ]
