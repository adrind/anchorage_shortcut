# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 19:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0061_remove_tasklist_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='steppage',
            name='icon',
        ),
    ]