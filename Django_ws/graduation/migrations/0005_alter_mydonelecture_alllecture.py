# Generated by Django 5.1.4 on 2025-02-02 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation', '0004_nowlecturedata_mydonelecture_nowlecture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mydonelecture',
            name='alllecture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='graduation.alllecturedata'),
        ),
    ]
