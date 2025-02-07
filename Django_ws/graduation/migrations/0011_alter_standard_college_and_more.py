# Generated by Django 5.1.4 on 2025-02-04 21:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "graduation",
            "0010_standard_college_standard_general_essential_credit_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="standard",
            name="college",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="standard",
            name="general_essential_credit",
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
        migrations.AlterField(
            model_name="standard",
            name="major_credit",
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
        migrations.AlterField(
            model_name="standard",
            name="rest_credit",
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name="standard",
            name="year",
            field=models.CharField(max_length=30),
        ),
    ]
