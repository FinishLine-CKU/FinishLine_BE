# Generated by Django 5.1.4 on 2025-01-22 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mydonelecture',
            name='lecture_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
