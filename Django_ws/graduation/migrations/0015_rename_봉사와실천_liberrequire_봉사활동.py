# Generated by Django 5.1.4 on 2025-02-06 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graduation', '0014_alter_mydonelecture_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='liberrequire',
            old_name='봉사와실천',
            new_name='봉사활동',
        ),
    ]
