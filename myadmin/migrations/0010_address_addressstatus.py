# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-24 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0009_orderinfo_goodid'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='addressstatus',
            field=models.IntegerField(default=0),
        ),
    ]
