# Generated by Django 4.2.16 on 2024-10-04 08:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ervaringsdeskundige', '0003_alter_user_salt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='beschikbaar_vanaf',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
