# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-12 18:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0046_auto_20170711_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadmapfrequentlyaskedquestions',
            name='page_url',
            field=models.URLField(default=''),
        ),
        migrations.AddField(
            model_name='steppagefrequentlyaskedquestions',
            name='page_url',
            field=models.URLField(default=''),
        ),
        migrations.AddField(
            model_name='tasklistfrequentlyaskedquestions',
            name='page_url',
            field=models.URLField(default=''),
        ),
    ]