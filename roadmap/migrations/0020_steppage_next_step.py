# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 21:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0019_auto_20170622_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='steppage',
            name='next_step',
            field=models.URLField(blank=True),
        ),
    ]
