# Generated by Django 3.0.3 on 2020-03-01 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_merge_20200228_2253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['date_posted']},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
    ]
