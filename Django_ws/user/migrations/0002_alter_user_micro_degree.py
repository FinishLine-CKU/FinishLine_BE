# Generated by Django 5.1.4 on 2025-01-09 16:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="micro_degree",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
