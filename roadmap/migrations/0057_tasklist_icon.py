# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-16 06:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('roadmap', '0056_contact_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklist',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]