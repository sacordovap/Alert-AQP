# Generated by Django 3.2.8 on 2021-10-30 21:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_alter_incidente_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidente',
            name='hora',
            field=models.TimeField(default=datetime.datetime, null=True),
        ),
    ]
