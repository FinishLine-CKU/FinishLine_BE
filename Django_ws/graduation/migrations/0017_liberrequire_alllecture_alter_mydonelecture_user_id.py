# Generated by Django 5.1.4 on 2025-02-07 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation', '0016_merge_20250208_0509'),
    ]

    operations = [
        migrations.AddField(
            model_name='liberrequire',
            name='alllecture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='graduation.alllecturedata'),
        ),
        migrations.AlterField(
            model_name='mydonelecture',
            name='user_id',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
