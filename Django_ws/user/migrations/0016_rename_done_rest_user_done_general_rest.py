# Generated by Django 5.1.4 on 2025-04-03 05:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0015_alter_user_last_login"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="done_rest",
            new_name="done_general_rest",
        ),
    ]
