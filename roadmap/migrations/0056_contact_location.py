# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0055_auto_20170811_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='location',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]