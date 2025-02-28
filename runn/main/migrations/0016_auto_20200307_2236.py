# Generated by Django 3.0.3 on 2020-03-08 06:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20200307_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='distance',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.1)]),
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.TimeField(help_text='Enter time in the form "HH:MM:SS".'),
        ),
    ]
