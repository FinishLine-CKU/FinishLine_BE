# Generated by Django 5.1.4 on 2025-04-10 14:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0017_user_done_rest"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="need_major",
            new_name="lack_major",
        ),
    ]
