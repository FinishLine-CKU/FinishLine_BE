# Generated by Django 5.1.4 on 2025-03-14 17:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_visitorcount'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_time_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
