# Generated by Django 5.1.4 on 2025-04-13 17:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0020_rename_done_micro_degree_user_done_md"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="done_sub_major_rest",
            field=models.DecimalField(
                blank=True, decimal_places=1, max_digits=5, null=True
            ),
        ),
    ]
