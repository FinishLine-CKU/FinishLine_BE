# Generated by Django 5.1.4 on 2025-04-10 16:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("graduation", "0029_rename_rest_credit_standard_rest_standard"),
    ]

    operations = [
        migrations.RenameField(
            model_name="standard",
            old_name="sub_major_credit",
            new_name="sub_major_standard",
        ),
    ]
