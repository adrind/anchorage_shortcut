# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 21:36
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0064_remove_steppage_icon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roadmap',
            old_name='body',
            new_name='mission_statement',
        ),
        migrations.AddField(
            model_name='roadmap',
            name='testimonials',
            field=wagtail.wagtailcore.fields.StreamField((('testimonial', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock()), ('name', wagtail.wagtailcore.blocks.CharBlock())))),), blank=True, default=[]),
        ),
        migrations.AlterField(
            model_name='roadmap',
            name='sections',
            field=wagtail.wagtailcore.fields.StreamField((('section', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('pages', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.PageChooserBlock())), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())))),)),
        ),
    ]
