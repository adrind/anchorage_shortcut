# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 21:58
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0026_tasklist_istemplatea'),
    ]

    operations = [
        migrations.AddField(
            model_name='steppage',
            name='short_description',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
    ]