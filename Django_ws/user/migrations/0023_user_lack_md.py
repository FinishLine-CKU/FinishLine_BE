# Generated by Django 5.1.4 on 2025-04-17 22:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0022_rename_micro_degree_user_md_user_done_md_rest"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="lack_MD",
            field=models.DecimalField(
                blank=True, decimal_places=1, max_digits=5, null=True
            ),
        ),
    ]
