# Generated by Django 5.1.4 on 2025-04-10 15:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "graduation",
            "0027_rename_general_essential_credit_standard_essential_ge_standatd",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="standard",
            old_name="general_selection_credit",
            new_name="choice_GE_standard",
        ),
    ]
