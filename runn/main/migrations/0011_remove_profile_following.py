# Generated by Django 3.0.3 on 2020-03-01 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_profile_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='following',
        ),
    ]
