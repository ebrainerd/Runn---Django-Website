# Generated by Django 3.0.2 on 2020-02-25 01:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_profile_user_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['date_posted']},
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main.Post'),
            preserve_default=False,
        ),
    ]
