# Generated by Django 4.2.2 on 2023-06-24 16:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userDashboard', '0007_remove_user_time_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
