# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 00:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('home', '0004_auto_20170914_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='testimonials',
        ),
        migrations.AddField(
            model_name='homepage',
            name='website_icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
