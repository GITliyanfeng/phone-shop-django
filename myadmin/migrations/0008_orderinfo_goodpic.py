# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-22 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0007_auto_20180920_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='goodpic',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
