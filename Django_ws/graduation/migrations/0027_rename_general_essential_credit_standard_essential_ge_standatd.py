# Generated by Django 5.1.4 on 2025-04-10 15:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("graduation", "0026_rename_major_credit_standard_major_standard"),
    ]

    operations = [
        migrations.RenameField(
            model_name="standard",
            old_name="general_essential_credit",
            new_name="essential_GE_standatd",
        ),
    ]
