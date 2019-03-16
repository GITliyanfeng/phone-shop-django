# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-20 19:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0005_auto_20180917_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addressname', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=50)),
                ('addressphone', models.CharField(max_length=11)),
                ('isdefault', models.BooleanField(default=False)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Users')),
            ],
        ),
        migrations.AddField(
            model_name='types',
            name='topbar',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='goods',
            name='pointnum',
            field=models.IntegerField(default=0),
        ),
    ]