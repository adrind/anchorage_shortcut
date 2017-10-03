# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-03 00:10
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_sitesettings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='website_footer',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='website_header_icon',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='website_header_text',
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='website_footer',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
    ]
