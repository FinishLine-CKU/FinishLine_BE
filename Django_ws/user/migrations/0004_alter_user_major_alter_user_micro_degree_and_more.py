# Generated by Django 5.1.4 on 2025-01-09 16:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_alter_user_micro_degree_alter_user_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="major",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="user",
            name="micro_degree",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="user",
            name="student_id",
            field=models.CharField(
                max_length=30, primary_key=True, serialize=False, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="sub_major",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="sub_major_type",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]