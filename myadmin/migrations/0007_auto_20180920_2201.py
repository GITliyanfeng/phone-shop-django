# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-20 22:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0006_auto_20180920_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goodname', models.CharField(max_length=30)),
                ('goodprice', models.FloatField()),
                ('goodnum', models.IntegerField()),
                ('goodsubtotal', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Oredr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addtime', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=0)),
                ('total', models.FloatField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Address')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Users')),
            ],
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='oid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Oredr'),
        ),
    ]
