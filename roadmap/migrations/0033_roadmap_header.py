# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-28 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0032_auto_20170628_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadmap',
            name='header',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
