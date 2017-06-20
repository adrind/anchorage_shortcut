# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 23:07
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0007_auto_20170620_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklist',
            name='choice_list',
            field=wagtail.wagtailcore.fields.StreamField([(b'question', wagtail.wagtailcore.blocks.CharBlock()), (b'choices', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([('name', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('label', wagtail.wagtailcore.blocks.CharBlock(required=True))], template='roadmap/content_blocks/choice_form.html')))]),
        ),
    ]
